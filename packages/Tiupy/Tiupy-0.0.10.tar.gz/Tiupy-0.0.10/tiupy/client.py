from requests import Session as Http
from .ext.utilities import headers, exceptions, objects

class Client:
    def __init__(self, proxies: dict = None, user_agent: str = None, certificatePath: bool = None, requestTimeout: int = 120):
        """
        Initialize the Client object.

        Args:
            proxies (dict, optional): Proxies configuration for HTTP requests.
            user_agent (str, optional): User agent string to be used in headers.
            certificatePath (bool, optional): Path to SSL certificate file.
            requestTimeout (int, optional): Request timeout in seconds.
        """

        self.api = "https://my.tiu.edu.iq"
        self._is_authenticated = False
        self.sid = None
        self.proxies = proxies
        self.user_agent = user_agent
        self.request = Http().request
        self.certificatePath = certificatePath
        self.requestTimeOut = requestTimeout
        self.profile: objects.UserProfile = objects.UserProfile(None)


    def _get_profile_info(self):
        """
        Retrieve profile information.
        
        Returns:
            str: Profile information response.
        """

        response = self.request("GET", f"{self.api}/pages/home.php", headers=self.parse_headers(), proxies=self.proxies, verify=self.certificatePath, timeout=self.requestTimeOut)
        return response.text
    


    def _require_authentication(func):
        """
        Decorator to require authentication before executing the function.

        Args:
            func (callable): The function to be decorated.

        Returns:
            callable: The decorated function.

        Raises:
            exceptions.CheckException: If the user is not authenticated.
        """
        def wrapper(self, *args, **kwargs):
            if not self._is_authenticated:
                raise exceptions.CheckException(401)
            return func(self, *args, **kwargs)
        return wrapper


    

    def parse_headers(self):
        """
        Generate headers with user agent information.

        Returns:
            dict: Headers for HTTP requests.
        """

        if self.user_agent:
            return headers.Headers(self.user_agent).headers
        
        else:
            return headers.Headers().headers

    def sid_login(self, SID: str):
        """
        Log in using an existing session ID.

        Args:
            SID (str): Session ID.
        """

        self._is_authenticated = True
        self.sid = SID
        headers.sid = self.sid
        self.profile = objects.UserProfile(self._get_profile_info())

        return

    def login(self, username: str, password: str):
        """
        Perform login with the provided username and password.

        Args:
            username (str): Username.
            password (str): Password.

        Returns:
            int: The status code of the login request.

        Raises:
            exceptions.CheckException: If the login request fails.
        """

        data = {
            'username': username,
            'password': password,
            'login.x': '0',  # Need to change?
            'login.y': '0'   # Need to change?
        }

        response = self.request("POST", url=f"{self.api}/", headers=self.parse_headers(), data=data, proxies=self.proxies, verify=self.certificatePath, timeout=self.requestTimeOut)

        if response.status_code != 200:
            return exceptions.CheckException(response.status_code)

        self._is_authenticated = True
        self.sid = response.cookies.get("PHPSESSID")
        headers.sid = self.sid
        self.profile = objects.UserProfile(self._get_profile_info())

        return response.status_code

    def logout(self):
        """
        Logout from the current session.

        Returns:
            int: The status code of the logout request.

        Raises:
            exceptions.CheckException: If the logout request fails.
        """

        response = self.request("GET", f"{self.api}/pages/p999.php/", headers=self.parse_headers(), proxies=self.proxies, verify=self.certificatePath, timeout=self.requestTimeOut)

        if response.status_code != 200:
            raise exceptions.CheckException(response.status_code)

        self._is_authenticated = False
        self.sid = None
        headers.sid = None

        return response.status_code
    

    @_require_authentication
    def get_courses_data(self):
        """
        Retrieve courses data.

        Returns:
            objects.CourseData: Course data response.

        Raises:
            exceptions.CheckException: If the request to retrieve course data fails.
        """

        response = self.request("GET", f"{self.api}/pages/p103.php", headers=self.parse_headers(), proxies=self.proxies, verify=self.certificatePath, timeout=self.requestTimeOut)

        if response.status_code != 200:
            raise exceptions.CheckException(response.status_code)
        
        return objects.CourseData(response.text)
