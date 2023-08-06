# github_downloader
This python program will let you download specific folders from any  github repository.




<!-- To download any github folder send get request to http://gitdl.onrender.com/url/{link_of_folder}     
here link of folder should be modified as below
  https://github.com/microsoft/terminal/tree/main/.config
  should be modified as
  github.com microsoft terminal tree main .config


3
for hhljkl;'
lkhkhghjkhklj:lhhwtesting this file is edited
 
there is one more way to use it
send post request to http://gitdl.onrender.com/get_add with {'url': "unmodified_url_of_the_folder"} 
response of this will be text (say config)
now send get to http://gitdl.onrender.com/download/{response_text} here response is config so url will be 
http://gitdl.onrender.com/download/config -->
     
 
<!-- To test it you can head to http://gitdl.onrender.com/docs -->



This project is still in development so as of now
 it cannot download whole repo or just a  single file(only a folder i.e. all internal folders and it's all files)
 It will give errors when a non github link is provided.

Todo
make this a python cli instead of a webapp 
