#   Copyright ETH 2018 - 2023 Zürich, Scientific IT Services
# 
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
# 
#        http://www.apache.org/licenses/LICENSE-2.0
#   
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
import re
import time

import pytest

from pybis import Openbis


def test_token(openbis_instance):
    assert openbis_instance.token is not None
    assert openbis_instance.is_token_valid(openbis_instance.token) is True
    assert openbis_instance.is_session_active() is True


def test_http_only(openbis_instance):
    with pytest.raises(Exception):
        new_instance = Openbis("http://localhost")
        assert new_instance is None

    new_instance = Openbis(
        url="http://localhost",
        allow_http_but_do_not_use_this_in_production_and_only_within_safe_networks=True,
    )
    assert new_instance is not None


def test_cached_token(other_openbis_instance):
    assert other_openbis_instance.is_token_valid() is True

    other_openbis_instance.logout()
    assert other_openbis_instance.is_token_valid() is False


def test_create_perm_id(openbis_instance):
    permId = openbis_instance.create_permId()
    assert permId is not None
    m = re.search("([0-9]){17}-([0-9]*)", permId)
    ts = m.group(0)
    assert ts is not None
    count = m.group(1)
    assert count is not None


def test_get_samples_update_in_transaction(openbis_instance):
    """
        Update samples in transaction without overriding parents/children
    """
    name_suffix = str(time.time())
    # Create new space
    space = openbis_instance.new_space(code='space_name' + name_suffix, description='')
    space.save()

    # Create new project
    project = space.new_project(code='project_code' + name_suffix)
    project.save()

    # Create new experiment
    experiment = openbis_instance.new_experiment(
        code='MY_NEW_EXPERIMENT',
        type='DEFAULT_EXPERIMENT',
        project=project.code
    )
    experiment.save()

    # Create parent sample
    sample1 = openbis_instance.new_sample(
        type='YEAST',
        space=space.code,
        experiment=experiment.identifier,
        parents=[],
        children=[],
        props={"$name": "sample1"}
    )
    sample1.save()

    # Create child sample
    sample2 = openbis_instance.new_sample(
        type='YEAST',
        space=space.code,
        experiment=experiment.identifier,
        parents=[sample1],
        children=[],
        props={"$name": "sample2"}
    )
    sample2.save()

    # Verify samples parent/child relationship
    sample1 = openbis_instance.get_sample(
        sample_ident=sample1.identifier,
        space=space.code,
        props="*"
    )
    sample2 = openbis_instance.get_sample(
        sample_ident=sample2.identifier,
        space=space.code,
        props="*"
    )
    assert sample1.children == [sample2.identifier]
    assert sample2.parents == [sample1.identifier]

    trans = openbis_instance.new_transaction()
    # get samples that have parents and update name
    samples = openbis_instance.get_samples(space=space.code, props="*", withParents="*")
    for sample in samples:
        sample.props["$name"] = 'new name for sample2'
        trans.add(sample)
    # get samples that have children and update name
    samples = openbis_instance.get_samples(space=space.code, props="*", withChildren="*")
    for sample in samples:
        sample.props["$name"] = 'new name for sample1'
        trans.add(sample)
    trans.commit()

    # Verify that name has been changed and parent/child relationship remains
    sample1 = openbis_instance.get_sample(
        sample_ident=sample1.identifier,
        space=space.code,
        props="*"
    )
    sample2 = openbis_instance.get_sample(
        sample_ident=sample2.identifier,
        space=space.code,
        props="*"
    )
    assert sample1.props["$name"] == 'new name for sample1'
    assert sample1.children == [sample2.identifier]
    assert sample2.props["$name"] == 'new name for sample2'
    assert sample2.parents == [sample1.identifier]

    trans = openbis_instance.new_transaction()
    # get samples with attributes and change name
    samples = openbis_instance.get_samples(space=space.code, attrs=["parents", "children"])
    for sample in samples:
        sample.props["$name"] = "default name"
        trans.add(sample)
    trans.commit()

    # Verify that name has been changed and parent/child relationship remains
    sample1 = openbis_instance.get_sample(
        sample_ident=sample1.identifier,
        space=space.code,
        props="*"
    )
    sample2 = openbis_instance.get_sample(
        sample_ident=sample2.identifier,
        space=space.code,
        props="*"
    )
    assert sample1.props["$name"] == 'default name'
    assert sample1.children == [sample2.identifier]
    assert sample2.props["$name"] == 'default name'
    assert sample2.parents == [sample1.identifier]

    sample3 = openbis_instance.new_sample(
        type='YEAST',
        space=space.code,
        experiment=experiment.identifier,
        parents=[],
        children=[],
        props={"$name": "sample3"}
    )
    sample3.save()

    trans = openbis_instance.new_transaction()
    # get sample1 without attributes and add sample3 as a parent
    samples = openbis_instance.get_samples(space=space.code, identifier=sample1.identifier)
    for sample in samples:
        sample.add_parents([sample3.identifier])
        trans.add(sample)
    # get sample2 without attributes and remove sample1 as a parent
    samples = openbis_instance.get_samples(space=space.code, identifier=sample2.identifier)
    for sample in samples:
        sample.del_parents([sample1.identifier])
        trans.add(sample)
    trans.commit()

    # Verify changes
    sample1 = openbis_instance.get_sample(
        sample_ident=sample1.identifier,
        space=space.code,
        props="*"
    )
    sample2 = openbis_instance.get_sample(
        sample_ident=sample2.identifier,
        space=space.code,
        props="*"
    )
    sample3 = openbis_instance.get_sample(
        sample_ident=sample3.identifier,
        space=space.code,
        props="*"
    )
    assert sample1.children == []
    assert sample1.parents == [sample3.identifier]
    assert sample2.parents == []
    assert sample3.children == [sample1.identifier]


def test_failed_second_login_raises_exception(openbis_instance):
    """
        Logins to openBIS using wrong username/password, PyBIS should raise exception
    """
    assert openbis_instance.is_session_active() is True

    try:
        openbis_instance.login('non_existing_username_for_test', 'abcdef')
        # Login should fail at this point
        assert False
    except ValueError as e:
        assert str(e) == "login to openBIS failed"


def test_set_token_accepts_personal_access_token_object(openbis_instance):
    """
        Verifies that set_token method accepts both permId and PersonalAccessToken object
    """
    assert openbis_instance.is_session_active() is True

    pat = openbis_instance.get_or_create_personal_access_token(sessionName="Project A")

    openbis_instance.set_token(pat, save_token=True)
    openbis_instance.set_token(pat.permId, save_token=True)

def try_doing(func: any):
    def wrapper(*args2, **kwargs):
        try:
            return func(*args2, **kwargs)
        except Exception as e:
            print(f"Error while doing {args2}: {e}")
    return wrapper

def test_pat():
    """
        Verifies that set_token method accepts both permId and PersonalAccessToken object
    """
    from pybis import Openbis
    base_url = "https://alaskowski:8443/"
    # base_url = "http://127.0.0.1:8888/"
    base_url = "https://openbis-sis-ci-sprint.ethz.ch/"
    # base_url = "https://openbis-empa-lab000.ethz.ch"
    openbis_instance = Openbis(
        url=base_url,
        verify_certificates=False,
        allow_http_but_do_not_use_this_in_production_and_only_within_safe_networks=True
    )

    token = openbis_instance.login('admin', 'changeit')
    # pat = openbis_instance.get_or_create_personal_access_token(sessionName="Project A")
    print(token)

    spaces = openbis_instance.get_spaces()
    print(spaces)

    name_suffix = str(time.time())
    sp_name = "SURFAC_MICHAL.GORA_AT_EMPA.CH" + name_suffix

    sc = "TEST_" + name_suffix
    sc = "SURFAC_MICHAL.GORA_AT_EMPA.CH"

    pc = "ESFA_" + name_suffix
    ptc1 = "START_DATE_" + name_suffix
    ptc2 = "EXP_DESCRIPTION_" + name_suffix
    stc = "EXPERIMENTAL_STEP_MILAR_" + name_suffix

    # Create the new space and project
    # sp = openbis_instance.new_space(code=sc, description="Test space")
    # try_doing(sp.save)()
    pr = openbis_instance.new_project(code=pc, space=sc, description="ESFA experiments")
    try_doing(pr.save)()
    # Create the experiment
    exp = openbis_instance.new_collection(code=pc, project="/"+sc+"/"+pc, type="COLLECTION")
    try_doing(exp.save)()
    # Create the sample type
    date_prop = openbis_instance.new_property_type(code=ptc1, dataType="TIMESTAMP", label="Start date",
                                     description="Date of the measurement")
    try_doing(date_prop.save)()
    date_prop = openbis_instance.new_property_type(code=ptc2, dataType="MULTILINE_VARCHAR",
                                     label="Experimental description",
                                     description="Experimental description")
    try_doing(date_prop.save)()
    st = try_doing(openbis_instance.new_sample_type)(code=stc,
                                       generatedCodePrefix="EXSTEPMILAR")

    try_doing(st.save)()
    if st is None:
        print(openbis_instance.get_sample_types())
        st = openbis_instance.get_sample_type(stc)
        try_doing(st.save)()
    try_doing(st.assign_property)(ptc1)
    try_doing(st.assign_property)(ptc2)
    try_doing(st.assign_property)("$NAME")
    try_doing(st.save)()


    print("END")

def test_new_sample_user_rights():
    from pybis import Openbis
    base_url = "https://alaskowski:8443/"
    base_url = "http://127.0.0.1:8888/"
    # base_url = "https://openbis-sis-ci-sprint.ethz.ch/"
    # base_url = "https://openbis-empa-lab000.ethz.ch"
    openbis_instance = Openbis(
        url=base_url,
        verify_certificates=False,
        allow_http_but_do_not_use_this_in_production_and_only_within_safe_networks=True
    )

    token = openbis_instance.login('admin', 'changeit')
    # pat = openbis_instance.get_or_create_personal_access_token(sessionName="Project A")
    print(token)

    sample = openbis_instance.get_sample('20230622180232519-25')
    print("Before", sample.parents, sample.children)
    item = str(sample.children[0])
    sample.del_children([str(sample.children[0]), str(sample.children[2])])

    # pat = openbis_instance.get_or_create_personal_access_token(sessionName="Test Project")
    # exp = openbis_instance.get_experiment("20230607102400512-23")

    # samples = openbis_instance.get_samples(space='TEST_SPACE')
    # print(samples)
    #
    # sample = openbis_instance.new_sample(
    #     type='ENTRY',
    #     space='TEST_SPACE',
    #     # project='/TEST_SPACE/PROJECT_101',
    #     experiment='/TEST_SPACE/PROJECT_101/PROJECT_101_EXP_1',
    #     props={"$name": "some name"}
    # )
    # sample.save()


    print("END")


def test_dataset_fail():
    from pybis import Openbis
    base_url = "https://alaskowski:8443/"
    # base_url = "http://127.0.0.1:8888/"
    # base_url = "https://openbis-sis-ci-sprint.ethz.ch/"
    # base_url = "https://openbis-empa-lab000.ethz.ch"
    openbis_instance = Openbis(
        url=base_url,
        verify_certificates=False,
        allow_http_but_do_not_use_this_in_production_and_only_within_safe_networks=True
    )

    token = openbis_instance.login('admin', 'changeit')
    print(token)

    # bigfile
    # dataset = openbis_instance.get_dataset('20230627220058944-33')
    # smallfile
    # dataset = openbis_instance.get_dataset('20230628152519246-34')
    # dataset.download(destination='~/Downloads/tmp', wait_until_finished=True)

    exp = openbis_instance.get_experiment('20230713114432363-51')
    # exp.props['vocab'] = ['T1', 'T2', 'T3']
    exp.props['test'] = 'cross'
    exp.save()

    print("END")