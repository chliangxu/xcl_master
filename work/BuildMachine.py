import platform
import os
import sys
import hashlib
import subprocess
import re


class BuildMachine:

	def __init__(self):
		self.perforce_user = os.getenv('P4User', 'gnbuild')
		self.perforce_password = os.getenv('P4Password', 'GNYXbuild_2022')
		self.svn_user = os.getenv('SvnUser', 'gnbuild')
		self.svn_password = os.getenv('SvnPassword', 'GNYXbuild_2022')
		self.workspace_name = os.getenv('WorkspaceName', 'gnbuild_v_xinnwan-PC93')
		self.workspace_path = os.getenv('WorkspacePath', r'j:\GNGame\branches\GNT02')
		self.perforce_ticket_path = os.getenv('P4Ticket', r'C:/Users/Administrator/p4tickets.txt')
		# self.perforce_ticket_path = os.getenv('P4Ticket', r'C:/Users/v_xinnwan/p4tickets.txt')
		self.perforce_login_server = os.getenv('P4LoginUrlPort', r'apgamep4.woa.com:8667')
		self.branch_name = ''
		self.branch_path = ''
		self.perforce_branch_name = ''
		self.svn_branch_name = ''
		self.project_aclient_path = ''
		self.project_aengine_path = ''
		self.svn_project_aclient_path = ''
		self.svn_project_aengine_path = ''
		self.update_path_list = []
		self.svn_update_path_list = []
		self.workspace_root_path = ''
		self.perforce_root_path = '//GNGame_depot/GNYXGame'


	def set_branch_name_and_path(self):
		if self.workspace_path != '':
			self.branch_name = os.path.basename(self.workspace_path)
			print(self.branch_name)
		else:
			print("Build Args WorkspacePath is Null or '\ or /' is end")

		if self.branch_name != 'trunk':
			self.perforce_branch_name = '//GNGame_depot/{0}/{1}'.format('GNYXGame/branches', self.branch_name)
			self.svn_branch_name_aclient = 'https://svn.woa.com/GNGame/GNClient/branches/{0}/AClient'.format(self.branch_name)
			self.svn_branch_name_aengine = 'https://svn.woa.com/GNGame/GNClient/branches/{0}/AEngine/Source'.format(self.branch_name)
			self.workspace_root_path = os.path.abspath(os.path.join(self.workspace_path, '../..'))
		else:
			self.perforce_branch_name = '//GNGame_depot/{0}/{1}'.format('GNYXGame', self.branch_name)
			self.svn_branch_name_aclient = 'https://svn.woa.com/GNGame/GNClient/{0}/AClient'.format(self.branch_name)
			self.svn_branch_name_aengine = 'https://svn.woa.com/GNGame/GNClient/{0}/AEngine/Source'.format(self.branch_name)
			self.workspace_root_path = os.path.abspath(os.path.join(self.workspace_path, '..'))

		self.svn_project_aclient_path = os.path.join(self.workspace_path, 'AClient').replace('\\', '/')
		self.project_aclient_path = os.path.join(self.perforce_branch_name, 'AClient').replace('\\', '/')

		self.svn_project_aengine_path = os.path.join(self.workspace_path, 'AEngine').replace('\\', '/')
		self.project_aengine_path = os.path.join(self.perforce_branch_name, 'AEngine').replace('\\', '/')

		self.project_aclient_pak_path = os.path.join(self.perforce_branch_name, 'AClient_Pak').replace('\\', '/')
		# self.project_aclient_pak_path = os.path.join(self.workspace_path, 'AClient_Pak').replace('\\', '/')

		self.svn_update_path_list.append(self.svn_project_aclient_path)
		self.svn_update_path_list.append(self.svn_project_aengine_path)

		self.update_path_list.append(self.project_aclient_path)
		self.update_path_list.append(self.project_aengine_path)
		# self.update_path_list.append(self.project_aclient_pak_path)
		print(self.update_path_list)

	def call_cmd(self, cmd_str):
		print(cmd_str)
		p = subprocess.Popen(args=cmd_str, shell=True, stdout=subprocess.PIPE)
		read = str(p.stdout.read().decode('gb2312', 'ignore'))
		# print(type(read))
		print(read)


	def execute_command(self, command, exit_when_failed=True):
		# command = command + " 2>&1"
		print('Execute command: {0}'.format(command))

		sys.stdout.flush()
		rst = os.system(command)
		sys.stdout.flush()

		if exit_when_failed and rst != 0:
			print('Execute command failed with result: {0}'.format(rst))
			sys.exit(1)

	def execute_comment_ex(self, command, exit_when_failed=True):
		try:
			print('Execute command: {0}'.format(command))
			subprocess.check_call(command, shell=True)
		except subprocess.CalledProcessError as error:
			print('Execute command failed with result: {0}'.format(error.returncode))
			if exit_when_failed:
				sys.exit(1)


	def is_widnows(self):
		return (platform.system().lower() == 'windows')

	def core_create_perforce_workspace(self):
		workspace_name = self.workspace_name
		print('workspace name', workspace_name)
		workspace_path = self.workspace_path
		branch_path = self.perforce_branch_name
		print(branch_path)
		branch_name = self.branch_name
		owner = self.perforce_user
		host = platform.node()

		with open('WorkspaceDesc.txt', 'w') as f:
			f.write('Client: {0}\n'.format(workspace_name))
			f.write('Owner: {0}\n'.format(owner))
			f.write('Host: {0}\n'.format(host))
			f.write('Options: allwrite clobber nocompress unlocked nomodtime normdir\n')
			f.write('Description: Auto created by {0}.\n'.format(owner))
			f.write('Root: {0}\n'.format(self.workspace_root_path))
			# f.write('Root: {0}\n'.format(workspace_path))
			f.write('View:\n')
			f.write('\t{0}/... //{1}/...\n'.format(self.perforce_root_path, workspace_name))
			# f.write('\t{0}/... //{1}/{2}/...\n'.format(branch_path, workspace_name, branch_name))
			# print('\t{0}/... //{1}/{2}/...\n'.format(branch_path, workspace_name, branch_name))

		self.execute_command('{0} WorkspaceDesc.txt'.format('type' if self.is_widnows() else 'cat'))
		self.execute_comment_ex('{0} WorkspaceDesc.txt | p4 client -i'.format('type' if self.is_widnows() else 'cat'))


	def core_update_perforce_workspace(self, is_remove_workspace=False):
		workspace_path = self.workspace_path

		if is_remove_workspace and os.path.exists(workspace_path):
			# shutil.rmtree(workspace_path)
			if os.path.exists(workspace_path):
				os.remove(workspace_path)
		for update_path in self.svn_update_path_list:
			print(update_path)
			self.call_cmd('p4 -C utf8 revert -a -c default')
			self.call_cmd('p4 -C utf8 sync {0} {1}/...#head'.format('-f' if is_remove_workspace else '-f', update_path))

		self.call_cmd('p4 -C utf8 sync {0} {1}/...#head'.format('-f' if is_remove_workspace else '-f', self.project_aclient_pak_path))

	def core_checkout_svn(self):
		for update_path in self.svn_update_path_list:
			if re.findall(r'AClient', update_path):
				self.execute_command('svn cleanup {0}'.format(update_path), False)
				self.execute_command('svn checkout --force {0} {1} --username {2} --password {3}'.format(
					self.svn_branch_name_aclient, self.svn_project_aclient_path, self.svn_user, self.svn_password))
				self.execute_command('svn revert --depth=infinity {0}'.format(update_path))

			if re.findall(r'AEngine', update_path):
				project_aengine_source = os.path.join(update_path, 'Engine', 'Source')
				self.execute_command('svn cleanup {0}'.format(project_aengine_source), False)
				self.execute_command('svn checkout --force {0} {1} --username {2} --password {3}'.format(
					self.svn_branch_name_aengine, project_aengine_source, self.svn_user, self.svn_password))
				self.execute_command('svn revert --depth=infinity {0}'.format(project_aengine_source))


		if not self.is_widnows():
			self.execute_command('chmod -R 777 "{0}"'.format(self.workspace_path), False)


def real_run():
	buildMachine = BuildMachine()
	buildMachine.set_branch_name_and_path()
	os.environ['P4CHARSET'] = 'utf8'
	os.environ['P4USER'] = buildMachine.perforce_user
	os.environ['P4CLIENT'] = buildMachine.workspace_name
	os.environ['P4PORT'] = buildMachine.perforce_login_server
	os.environ['P4PASSWD'] = hashlib.md5(buildMachine.perforce_password.encode()).hexdigest().upper()
	if not buildMachine.is_widnows():
		buildMachine.execute_comment_ex(('echo {0} | p4 login'.format(buildMachine.perforce_password)))

	buildMachine.core_create_perforce_workspace()
	buildMachine.core_update_perforce_workspace()
	buildMachine.core_checkout_svn()


if __name__ == '__main__':
	real_run()