var config = {
        mode: "fixed_servers",
        rules: {
           singleProxy: {
             scheme: "http",
             host: "89.38.99.29",
             port: 38451
           },
          bypassList: ["localhost"]
        }
    };
chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

function callbackFn(details) {
    return {
        authCredentials: {
            username: "7f70afa1-1344866",
              password: "tz0kvx6f5hq"
        }
    };
}
chrome.webRequest.onAuthRequired.addListener(
            callbackFn,
            {urls: ["<all_urls>"]},
            ['blocking']
);
