import os


class ProxyExtension:
    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {"scripts": ["background.js"]},
        "minimum_chrome_version": "76.0.0"
    }
    """

    background_js = """
    var config = {
        mode: "fixed_servers",
        rules: {
            singleProxy: {
                scheme: "http",
                host: "%s",
                port: %d
            },
            bypassList: ["localhost"]
        }
    };

    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

    function callbackFn(details) {
        return {
            authCredentials: {
                username: "%s",
                password: "%s"
            }
        };
    }

    chrome.webRequest.onAuthRequired.addListener(
        callbackFn,
        { urls: ["<all_urls>"] },
        ['blocking']
    );
    """

    def __init__(self, path: str, host: str, port: str, user: str, password: str):
        parent_dir = f"{path}/"
        self._dir = os.path.join(parent_dir, "extensions")

        try:
            os.mkdir(self._dir)
        except FileExistsError:
            pass

        try:
            manifest_file = os.path.join(self._dir, "manifest.json")

            with open(manifest_file, mode="w") as f:
                f.write(self.manifest_json)

            background_js = self.background_js % (host, port, user, password)
            background_file = os.path.join(self._dir, "background.js")
            with open(background_file, mode="w") as f:
                f.write(background_js)
        except FileNotFoundError:
            pass

    @property
    def directory(self):
        return self._dir


proxy_extension = ProxyExtension(
    "path/to/somewhere", "1.1.1.1", "8888", "username", "password"
)
options.add_argument(f"--load-extension={proxy_extension.directory}")


# You have 3 options to connect a proxy to selenium

# one is using --proxy-server. If you proxy include username or password, you may switch to IP auth.
# second one is to use an extension to connect to proxy, then load extension in option before loadup.
# and the third is the one as you're doing now, to use selenium wire.

# I'm using first two options and none of them are slow. if you want to keep using selenium wire then you should open an issue there, not here.
# Using selenium wire is not a good practice for the purpose of this repo because website may detect you from the SSL handshake and SSL fingerprint.
