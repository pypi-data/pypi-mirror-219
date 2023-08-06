import os
import sys
from blendedUx.blended_flask.blended_hostlib.backend import FileSystemBackend
from blendedUx.blended_flask.blended_hostlib.network import Network
from blendedUx.blended_flask.blended_hostlib.controller import Controller
from blendedUx.blended_flask.blended_hostlib.exceptions import BlendedException, \
    PackageNameExistsException, AccountActivationException


class Route(object):
    """
    This is route class, an intermediary between CLI and Hostlib.
    """
    def __init__(self, account, package):
        """
        Initialization method of Route class.
        """
        blended_dir = account.blended_dir
        self.user_slug = account.user_slug
        self.current_account = account.current_account
        last_active = account.last_active
        current_dir = account.current_dir
        self.backend = FileSystemBackend(
                 current_dir, blended_dir=blended_dir,
                 current_account=self.current_account, blended_directory_path=blended_dir,
                 last_login=last_active)
        self.controller = Controller(Network(), self.backend)

    def sync_file_path(self, path_list):
        """
        The sync_file_path function is used to sync file_path.
        With particular os(windows, ubuntu, mac).When we use file flag in pull/push.
        """
        new_path_list = []
        for item in path_list:
            item = item.replace('/', os.sep)
            new_path_list.append(item)
        return new_path_list

    def install_package(self, account, package):
        """
        Adds/install the specified package into the local dependencies directory (lib).
        If no label is specified, then the canonical snapshot is assumed.
        This will recursively install all dependencies of the specified package as well.
        """
        package_name = package.package_name
        package_id = package.package_id
        label = package.label
        response = self.controller.install_package(package_name,
                                                   user_slug=self.user_slug,
                                                   label=label,
                                                   current_account=self.current_account)
        return response

    def create_package(self, account, package):
        """
        Creates a new package.
        """
        package_name = package.package_name
        package_title = package.package_title
        package_description = package.package_description
        package_type_name = package.package_type_name
        primary_category = package.primary_category
        secondary_category = package.secondary_category
        response, error_list = self.controller.create_package(self.current_account,
                                                              package_name,
                                                              package_type_name,
                                                              package_description,
                                                              package_title,
                                                              primary_category,
                                                              secondary_category)
        return response, error_list

    def packages_list(self, account, package):
        """
        Lists all of the packages available to the current user in the current account,
        unless --account is specified,
        in which case the specified account's contents are specified.
        """
        account_name = account.account_name
        package_name = package.package_name
        share = package.share
        transfer_by_me = package.transfer_by_me
        transfer_to_me = package.transfer_to_me
        organization = package.organization
        published = package.published
        purchased = package.purchased
        response = None
        if self.current_account == 'anonymous':
            account_name = 'anonymous'
        if(not account_name):
            try:
                account_name = self.controller.get_current_account(self.user_slug).slug
            except BlendedException as exc:
                raise BlendedException(exc)
        if package_name:
            response = self.controller.package_accounts_list(account_name, package_name=package_name)
        else:
            response = self.controller.packages_list(account_name, transfer_to_me=transfer_to_me,
                                                transfer_by_me=transfer_by_me, share=share, 
                                                organization=organization, published=published,
                                                purchased=purchased)
        return response

    def get_package_acquisition(self, account, package):
        """
        Adds the specified package into the library of the current account;
        similar to clone, except that it links the account to a specific license of the specified package.
        """
        package_name = package.package_name
        new_name = package.new_name
        package_id = package.package_id
        license_name = package.license_name
        label = package.label
        response = self.controller.get_package_acquisition(
                            package_name, license_name=license_name,
                            new_name=new_name, current_account=self.current_account, label=label)
        return response

    def package_clone(self, account, package):
        """
        it clones a package if the name exists then new-name is required with --new-name flag.
        It pull package in local src.
        """
        cloned_package_name = package.cloned_package_name
        package_name = package.package_name
        new_name = package.new_name
        package_id = package.package_id
        package_title = package.package_title
        label = package.label
        no_download = package.no_download
        package_description = package.package_description
        draft = package.draft
        primary_category = package.primary_category
        secondary_category = package.secondary_category
        response = self.controller.package_clone(
                        package_name, new_name=new_name, draft=draft, label=label,
                        description=package_description, current_account=self.current_account,
                        package_title=package_title, primary_category=primary_category,
                        secondary_category=secondary_category)
        return response
 
 
    def package_type(self, package_name, label, draft):
        """
        """
        package_name = package_name
        label = label
        draft = draft
        response = self.controller.get_type(
                        package_name, draft=draft, label=label,
                        current_account=self.current_account
                        )
        return response

    def package_extend(self, account, package):
        """
        A new package is created that includes the referenced package as a dependency, with an alias of "parent".
        """
        package_name = package.package_name
        new_name = package.new_name
        package_id = package.package_id
        label = package.label
        package_description = package.package_description
        draft = package.draft
        package_type = package.package_type
        package_title = package.package_title
        response = self.controller.package_extend(package_name,
                                                  new_name=new_name,
                                                  draft=draft,
                                                  label=label,
                                                  description=package_description,
                                                  current_account=self.current_account,
                                                  package_type=package_type,
                                                  package_title=package_title,
                                                  )
        return response

    def pull_package(self, account, package, **kwargs):
        """
        Downloads the specified package into blended/src, and all dependencies into either blended/lib or
        blended/src, depending on the rules. clone internally call pull_package with "new_name".
        """
        hub_pack = kwargs.get('pack', None)
        package_name = package.package_name
        package_id = package.package_id
        label = package.label
        draft = package.draft
        update = package.update
        force = package.force
        files = package.files
        new_name = package.new_name
        if new_name:
            package_name = new_name
        replace_from_local_list = package.replace_from_local_list
        if label:
            try:
                response = self.controller.package_clone(
                        package_name, new_name=new_name, draft=False, label=label,
                        description=None, current_account=self.current_account, action="pull")
            except BlendedException as exc:
                try:
                    raise BlendedException(exc.args[0].args[0].args[0])
                except IndexError:
                    raise BlendedException(exc)
            return response
        if files:
            response = self.controller.pull_package(package_name,
                                               force, draft=draft, user_slug=self.user_slug,
                                               label=label, current_account=self.current_account, files=files)
        elif replace_from_local_list:
            location = []
            for item in replace_from_local_list:
                location.append((item.location.split(package_name)[1].lstrip(os.sep)).replace(os.sep, "/"))
            response = self.controller.pull_package(package_name,
                                               force, draft=draft, user_slug=self.user_slug,
                                               label=label, current_account=self.current_account,
                                               files=location)
        else:
            response = self.controller.pull_package(package_name,
                                               force, draft=draft, user_slug=self.user_slug,
                                               label=label, current_account=self.current_account)
        return response

    def push_package(self, account, package, **kwargs):
        """
        Pushes the local package up to the hub, provided there are no conflicts.
        If a list of files/file paths is specified after the --files flag,
        then only those files are pushed up. It print conflicts files.
        --force causes remote files to be overwritten with no warning.
        """
        error_list = []
        pack = kwargs.get('pack', None)
        files = package.files
        package_name = package.package_name
        package_id = package.package_id
        force = package.force
        replace_from_hub_list = package.replace_from_hub_list
        if replace_from_hub_list:
            if files:
                result = self.controller.as_jptf(replace_from_hub_list)
            else:
                result = self.controller.as_partial_jptf(replace_from_hub_list, pack)
            response = self.controller.push_package(
                       package_name, force=force, user_slug=self.user_slug,
                       replace_from_hub_list=result, current_account=self.current_account)
        elif files:
            response = self.controller.push_package(package_name, force=force, user_slug=self.user_slug,
                                               files=files, current_account=self.current_account)
        else:
            try:
                response = self.controller.push_package(package_name, force=force, user_slug=self.user_slug, current_account=self.current_account)
            except BlendedException as exc:
                raise BlendedException(exc)
        if isinstance(response, tuple):
            response, error_list = response
            if error_list:
                for image_name in error_list:
                    print("Some error in uploading image %s.\n" % (image_name))
        return response

    def compare_package(self, account, package):
        """
        If any differences are found, conflicts/differences are printed listing all of the files and their locations,
        and the command exits.
        """
        files = package.files
        package_name = package.package_name
        package_id = package.package_id
        label = package.label
        controller = self.controller
        backend = self.backend
        if package_name:
            identifiers = package_name.split("/")
            if len(identifiers) > 1:
                if (self.current_account == identifiers[0]):
                    package_name = identifiers[1]
                else:
                    raise BlendedException('Account name \"%s\" is not Current account or valid account.' % identifiers[0])

        try:
            hub_package = controller.network.download_draft(self.current_account, package_name, as_hashes="1")
            hub_jptf, package_hash, canonical_type = controller._remove_root_from_jptf(hub_package)
            if controller.backend.directory_path.endswith('src'):
                package_slug_temp = os.path.join(controller.backend.directory_path, package_slug)
            else:
                package_slug_temp = os.path.join(controller.backend.directory_path, controller.backend.src, package_name)

            hub_package = controller.de_jptf(hub_jptf, as_hashes=True, package_slug=package_slug_temp)
            hub_package = controller.backend.get_class('intermediary')(
                                                       package_name, content=hub_package,
                                                       name=package_name, hash=package_hash, as_hashes=True)
        except BlendedException as exc:
            raise BlendedException(exc)
        try:
            package = controller.backend.get_package(package_name)
        except BlendedException as exc:
            raise BlendedException(exc)
        local_last_hash = backend.get_hash(package_name)
        response = controller.compare_package(hub_package, package, local_last_hash, "compare")
        return response

    def update_package(self, account, package):
        """
        It updates package with another package except hash_file/_package.json.
        Update package in local not on the hub.
        """
        package_name = package.package_name
        source_package = package.source_package
        label = package.label
        package_id = package.package_id
        force = package.force
        response = self.controller.update_package(package_name, source_package,
                                                  current_account=self.current_account,
                                                  label=label, force=force)
        return response

    def get_versions_list(self, account, package):
        """
        It provides list of all snapshot version of a package.
        --canonical flag used to get the canonical version of a package.
        """
        package_name = package.package_name
        canonical = package.canonical
        package_id = package.package_id
        response = self.controller.package_version(self.current_account, package_name, canonical=canonical)
        return response

    def package_snapshot(self, account, package, **kwargs):
        """
        Creates a new version based on the current state of the draft.
        """
        auto_share_packages = kwargs.get('auto_share_packages', [])
        purchase_packages = kwargs.get('purchase_packages', [])
        skip_validation = package.skip_validation
        package_name = package.package_name
        label = package.label
        package_id = package.package_id
        response = self.controller.package_snapshot(self.current_account,package_name,label=label,
                                                    auto_share_packages=auto_share_packages, purchase_packages=purchase_packages, 
                                                    skip_validation=skip_validation)
        return response

    def package_canonical(self, account, package):
        """
        Markes the specified version as the cannonical version.
        """
        package_name = package.package_name
        label = package.label
        package_id = package.package_id
        response = self.controller.package_canonical(self.current_account, package_name, label=label)
        return response

    def package_share(self, account, package, **kwargs):
        """
        Makes the package available privately to the specified account to download and clone.
        """
        auto_share_packages = kwargs.get('auto_share_packages', [])
        package_name = package.package_name
        email = account.email
        account_name = account.account_name
        package_id = package.package_id
        get = package.get
        if auto_share_packages:
            response = self.controller.package_share(
                       self.current_account, package_name,
                       account_name=account_name, email=email,
                       auto_share_packages=auto_share_packages)
        else:
            response = self.controller.package_share(self.current_account,
                                                     package_name,
                                                     account_name=account_name,
                                                     email=email,
                                                     get=get)
        return response

    def package_transfer(self, account, package,  **kwargs):
        """
        Moves all licensing rights for a package from the current account to the specified account.
        """
        auto_share_packages = kwargs.get('auto_share_packages', [])
        purchase_packages = kwargs.get('purchase_packages', [])
        package_name = package.package_name
        email = account.email
        account_name = account.account_name
        package_id = package.package_id
        if auto_share_packages or purchase_packages:
            response = self.controller.package_transfer(self.current_account,
                                                        package_name,
                                                        account_name=account_name,
                                                        email=email,
                                                        auto_share_packages=auto_share_packages,
                                                        purchase_packages=purchase_packages)
        else:
            response = self.controller.package_transfer(self.current_account,
                                                        package_name,
                                                        account_name=account_name,
                                                        email=email)
        return response

    def package_as_json(self, account, package):
        """
        It gives json of package. For now It work only for local package.
        """
        package_name = package.package_name
        package_id = package.package_id
        identifiers = package_name.split("/")
        if len(identifiers) > 1:
            if (self.current_account == identifiers[0]):
                package_name = identifiers[1]
            else:
                raise BlendedException('Account name \"%s\" is not Current account or valid account.' % identifiers[0])
        try:
            package = self.controller.backend.get_package(package_name)
        except BlendedException as exc:
            raise BlendedException(exc)
        return self.controller.as_jptf(package)

    def package_detail(self, account, package):
        """
        Prints the details of the package in a nice format, with less-like up-and-down behavior.
        --description causes only the description of the package.
        --licenses lists all the licenses for the package.
        """
        package_name = package.package_name
        package_id = package.package_id
        is_description = package.is_description
        is_licenses = package.is_licenses
        response = self.controller.package_detail(self.current_account, package_name)
        return response

    def package_publish(self, account, package, **kwargs):
        """
        publication of package.
        """
        publication = kwargs.get('publication', [])
        package_name = package.package_name
        package_id = package.package_id
        canonical = package.canonical
        validate = package.validate
        get_publish = package.get
        response = self.controller.package_publication(
                            self.current_account, package_name, publication,
                            canonical=canonical, validate=validate, get_publish=get_publish
                            )
        return response

    def package_validate(self, account, package):
        """
        Creates a new package.
        """
        package_name = package.package_name
        package_id = package.package_id
        label = package.label
        response = self.controller.package_validate(self.current_account,
                                                    package_name,
                                                    label=label)
        return response
        
    def account_email_verification(self, email):
        """
        """
        response = self.controller.account_email_verification(email)
        return response

    def get_title(self, account_name, package_name):
        """
        """
        response = self.controller.get_title(account_name, package_name)
        return response
    
    def package_revoke(self, account, package):
        """
        Creates a new package.
        """
        package_name = package.package_name
        account_name = account.account_name
        share = package.share
        transfer = package.transfer
        package_id = package.package_id
        email = account.email
        response = self.controller.package_revoke(self.current_account,
                                                  package_name,
                                                  account_name,
                                                  email=email,
                                                  share=share,
                                                  transfer=transfer)
        return response

    def package_reject(self, account, package):
        """
        Reject package access.
        """
        package_name = package.package_name
        account_name = account.account_name
        share = package.share
        transfer = package.transfer
        package_id = package.package_id
        
        response = self.controller.package_reject(self.current_account,
                                                  package_name,
                                                  account_name,
                                                  share=share,
                                                  transfer=transfer)
        
        return response

    def package_accept(self, account, package):
        """
        Creates a new package.
        """
        package_name = package.package_name
        account_name = account.account_name
        new_name = package.new_name
        package_id = package.package_id
        
        response = self.controller.package_accept(self.current_account,
                                                  package_name,
                                                  account_name,
                                                  new_name=new_name)
        return response
        
    def check_package(self, account_name, package_name):
        """
        check package existence.
        """
        self.controller.check_package(account_name, package_name)
        