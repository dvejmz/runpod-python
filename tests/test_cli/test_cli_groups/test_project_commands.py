'''
RunPod | CLI | Groups | Project | Commands | Tests
'''
import unittest
from unittest.mock import patch

from click.testing import CliRunner
from runpod.cli.groups.project.commands import (
    new_project_wizard, launch_project_pod, start_project_pod)

class TestProjectCLI(unittest.TestCase):
    ''' A collection of tests for the Project CLI commands. '''

    def setUp(self):
        self.runner = CliRunner()

    def test_new_project_wizard_success(self):
        '''
        Tests the new_project_wizard command.
        '''
        with patch('click.prompt', return_value='XYZ_VOLUME') as mock_prompt, \
             patch('runpod.cli.groups.project.commands.validate_project_name') as mock_validate, \
             patch('click.confirm', return_value=True) as mock_confirm, \
             patch('runpod.cli.groups.project.commands.create_new_project') as mock_create:
            mock_validate.return_value = 'TestProject'
            result = self.runner.invoke(new_project_wizard, ['--name', 'TestProject', '--type', 'llama2', '--model', 'meta-llama/Llama-2-7b']) # pylint: disable=line-too-long

        mock_prompt.assert_called_with("Enter the ID of the volume to use", type=str)
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Project TestProject created successfully!", result.output)

    def test_new_project_wizard_invalid_name(self):
        '''
        Tests the new_project_wizard command with an invalid project name.
        '''
        result = self.runner.invoke(new_project_wizard, ['--name', 'Invalid/Name'])
        self.assertEqual(result.exit_code, 1)
        self.assertIn("Project name contains an invalid character", result.output)

    def test_launch_project_pod(self):
        '''
        Tests the launch_project_pod command.
        '''
        with patch('click.confirm', return_value=True) as mock_confirm, \
            patch('runpod.cli.groups.project.commands.launch_project') as mock_launch:
            result = self.runner.invoke(launch_project_pod)
        mock_confirm.assert_called_with("Do you want to continue?", abort=True)
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Launching project development environment...", result.output)
        mock_launch.assert_called_once()


    def test_start_project_pod(self):
        '''
        Tests the start_project_pod command.
        '''
        result = self.runner.invoke(start_project_pod, ['test_file.txt'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Starting project API server...", result.output)

    def test_start_project_pod_invalid_file(self):
        '''
        Tests the start_project_pod command with an invalid project file.
        '''
        result = self.runner.invoke(start_project_pod, ['nonexistent_file.txt'])
        self.assertEqual(result.exit_code, 1)
        self.assertIn("Error: Invalid value for 'project_file': Path 'nonexistent_file.txt' does not exist.", result.output) # pylint: disable=line-too-long
