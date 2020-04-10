#!/usr/bin/env python
#
# variales.py NAME BRANCH BUILDNO


import re
import os
import sys

name = sys.argv[1]
branch = sys.argv[2]
build = sys.argv[3]

# Set a Pipline variable
def set_variable(name, value):
    print(f'##vso[task.setvariable variable={name}]{value}')

if __name__ == '__main__':
    parent = None
    (branch_prefix, branch_name) = branch.rsplit('/', 1)

    tag = os.getenv('PROJECT_TAG', branch_name)
    if branch_prefix in ['refs/heads/feature', 'refs/heads/bugfix', 'refs/heads/hotfix']:
        set_variable('Project.DeploymentType', 'DEVELOPMENT')

        parent = 'dev'
        parent_branch = 'master'
        tag = re.compile('[A-Z]+-\\d+', re.I).match(branch_name).group()
        tag = 'latest'
        namespace = tag.lower()
        set_variable('Project.Tag', tag)
    else: # always consider as dev
        set_variable('Project.DeploymentType', 'DEVELOPMENT')

        parent = 'dev'
        parent_branch = 'master'
        # tag = re.compile('[A-Z]+-\\d+', re.I).match(branch_name).group()
        tag = 'latest'
        namespace = tag.lower()
        set_variable('Project.Tag', tag)
    # elif branch_prefix in ['refs/heads/release']:
    #     set_variable('Project.DeploymentType', 'RELEASE')

    #     parent = 'test'
    #     parent_branch = 'master'
    #     tag = branch_name
    #     namespace = tag.lower()
    #     set_variable('Project.Tag', tag)

    # else:
    #     set_variable('Project.DeploymentType', 'MASTER')

    #     parent_branch = branch_name
    #     namespace = tag.lower()

    set_variable('Project.ParentBranchName', parent_branch)
    set_variable('Project.Qualifier', tag.lower())
    set_variable('Project.QualifierAlphanum', tag.lower().replace('-','').replace('_',''))
    set_variable('Project.BuildTag', f'{tag}.{build}')

    set_variable('Helm.Namespace', namespace)
    set_variable('Helm.Release', f'{tag.lower()}.{name}')

    if parent != None:
        set_variable('AZDS.Space', f'{parent}/{namespace}')
        set_variable('AZDS.ParentSpace', parent)
        set_variable('AZDS.HostPrefix', f'{namespace}.s.{parent}')
    else:
        set_variable('AZDS.Space', namespace)
        set_variable('AZDS.ParentSpace', namespace)
        set_variable('AZDS.HostPrefix', namespace)
