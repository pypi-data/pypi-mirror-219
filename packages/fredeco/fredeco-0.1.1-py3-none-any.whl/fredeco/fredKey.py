def request_api_key():
    '''Get a FRED® API Key, from FRED® website.

        This function open the webpage where the user can request for a FRED® API Key. The API Key is necessary to use the current Python package
    
    '''
    import webbrowser
    webbrowser.open_new_tab('https://fredaccount.stlouisfed.org/apikeys')