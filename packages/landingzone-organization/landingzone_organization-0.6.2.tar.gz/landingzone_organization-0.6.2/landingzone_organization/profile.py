class Profile:
    def __init__(
        self,
        sso_start_url: str,
        sso_region: str,
        sso_role_name: str,
        role_session_name: str,
        account_name: str,
        account_id: str,
    ):
        self.sso_start_url = sso_start_url
        self.sso_region = sso_region
        self.sso_role_name = sso_role_name
        self.role_session_name = role_session_name
        self.account_name = account_name
        self.account_id = account_id

    def __eq__(self, other):
        return other and hash(self) == hash(other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(
            (
                self.sso_start_url,
                self.sso_region,
                self.account_id,
                self.account_name,
                self.sso_role_name,
                self.role_session_name,
            )
        )
