import requests
import urllib
import os
from PIL import Image
from bs4 import BeautifulSoup

def create_folders():
 if not os.path.exists("C:/Users/Fade/Desktop/Images"):
  print("Creating Folders...")
  os.makedirs("C:/Users/Fade/Desktop/Images")
  
  num_lines = sum(1 for lines in open('links.txt'))
  num = 0
  
  while num < num_lines:
   os.makedirs("C:/Users/Fade/Desktop/Images/" + str(num))
   num += 1
  
   

def scrape_images():
  print("Reading links.txt...")
  urls = open("links.txt").readlines()
  num_urls = sum(1 for lines in urls)
  urls_done = 0
  
  while urls_done < num_urls:
   print("Navigating to " + urls[urls_done])
   source = BeautifulSoup(requests.get(urls[urls_done]).text, "html.parser")
   
   print("Getting title...")
   listing_title = source.find("h1", {"id":"itemTitle"}).get_text()[16:].split(" ")
   print(listing_title)
   
   print("Getting image sources...")
   image_sources = []
   for images in source.findAll("img", {"onerror":"try{this.src='http://p.ebaystatic.com/aw/pics/cmp/icn/iconImgNA_96x96.gif';}catch(e){}"}):
      if not image_sources.__contains__(images.get("src")): #THIS PREVENTS DUPLICATES FROM BEING STORED
          image_sources.append(images.get("src"))
                   
                   
   save_images(image_sources, urls_done, listing_title)
   urls_done += 1
   print("----------------------------------")
        
        
        
def save_images(image_sources, urls_done, listing_title):
 print("Saving images...")
 for url in image_sources:
  if len(listing_title) <= 1:
   break
  else:
   urllib.request.urlretrieve(url[:51] + "00.jpg", "C:/Users/Fade/Desktop/Images/" + str(urls_done) + "/" + str(listing_title[0]) + "-" + str(listing_title[1]) + ".jpg")
   listing_title.remove(listing_title[1])
   listing_title.remove(listing_title[0])
   print(listing_title)
   
def resize_images():
 print("Resizing images...")
 
 for folders in os.listdir("C:/Users/Fade/Desktop/Images/"):
  for images in os.listdir("C:/Users/Fade/Desktop/Images/" + folders):
   new_image = Image.open("C:/Users/Fade/Desktop/Images/" + folders + "/" + images)
   new_image = new_image.resize((new_image.width * 2, new_image.height * 2), Image.ANTIALIAS)  
   new_image.save("C:/Users/Fade/Desktop/Images/" + folders + "/" + images) 
 
create_folders()
scrape_images()
resize_images()