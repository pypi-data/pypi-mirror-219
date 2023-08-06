class BlendedException(Exception):
    """
    Custom Exception for blendedcli,raise when something specific goes wrong.
    """
    pass


class AccountActivationException(Exception):
    """
    Custom Exception for inactive blended accounts if user try to logging it.
    """
    pass


class PackageNameExistsException(Exception):
    """
    Custom Exception raised if package name already exists in the account.
    """
    pass

