
# Save Pocket bookmarks to file on GitHub

Small script that gets links that are added to Pocket, and pushes new changes to a file on GitHub.

### How does it work?
1. I save articles I want to read on pocket.
1. On my server, I have a cronjob that runs a small script (main.py) that checks if anything new is added to my pocket list with the tag ‘public’.
1. If it finds something that was not added to my bookmarks page yet, it adds the new link to the file that contains my bookmarks and commits and pushes it to GitHub.
1. GitHub Pages makes sure that the new change is deployed to this website automatically.

### Installation 
1. Clone the repository 
1. Create an app on [pocket]([https://getpocket.com/developer/apps/new](https://getpocket.com/developer/apps/new)), store its consumer key
2. Install the requirements (just `python-dotenv` and `click`)  
```pip install -r requirements.txt```
3. Create an environment file
	 `cp .env.example .env`
	 Add your GitHub access code and Pocket consumer key
4. Run `python pocket_handler.py` and save the `access_token` to your  `.env` file. 
5. Add a `input_separator` to you `.env` file. The script will try to add new links after this point in your file. For example, I use `<ul>` as my input separator, and add new a `<li>` after that for each new link. You can change this setup in `main.py` `add_bookmark()`. 

You should now be able to run `python main.py` with the required input

### How to use
Once installed, you can call `main.py` with the following parameters:
```
main.py -i {file_to_edit} -r {repository_of_file} 
```
This fetches your latest additions to Pocket, adds them to the specified file and commits and pushes that change to GitHub.
