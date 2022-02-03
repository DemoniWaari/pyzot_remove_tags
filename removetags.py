from pyzotero import zotero
import secrets # Api key and ID from secrets.py

# Split list into chunks of n items
def chunks(l,n):
  for i in range(0, len(l), n):
    yield l[i:i+n]

# Make Zotero connection
def make_connection(id, api):
  library_type = 'user'
  return zotero.Zotero(id, library_type, api)

# Grab all tags and return all articles for a tag
# That the search is not case-sensitive!
# Add tags with only one article to-be-deleted list
def get_tags_and_filter(zot, taglist):
  all_tags = zot.everything(zot.tags())
  for t in all_tags:
    zot.add_parameters(tag=t) # Search by tag
    tag_items = zot.items()
    n_items = len(tag_items)
    print(f'tag:{t} n:{n_items}')
    if n_items == 1:
      taglist.append(t)
      print(f'\t Assined for deletion:')
  return taglist  

def write_to_file(taglist, myfile):
  # Write all tags to a file 
  print('Writing tags to file')
  with open(myfile,'w') as f:
    for t in taglist:
      f.write('%s\n' % t)

# Delete tags
def del_tags(zot, taglist):
  print(f'Deleting tags: {taglist}')
  # If more than 50 then we need to do a loopy loop
  if len(taglist) > 50:
    chunked = list(chunks(taglist, 50)) # Split list
    for l in chunked:
      zot.delete_tags(*l)
  else:
    zot.delete_tags(*taglist)
  n_tags = len(taglist)
  print(f'Deleted {n_tags} tags.')
  return 0

def main():
  # Do connection
  zot = make_connection(secrets.library_id, secrets.api_key)
  deleted_tags = [] # will be populated by tags with one article
  # Get to be deleted tags
  deleted_tags = get_tags_and_filter(zot, deleted_tags)
  # Write them to file just to be sure
  write_to_file(deleted_tags, 'deletetags.txt')
  # Delete them
  del_tags(zot, deleted_tags)
  
if __name__ == "__main__":
  main()
  
  

# Testing, returns tags of 5 newest articles
#def test(zot)
  #all_tags = []
  #items = zot.top(limit=5)
  #for item in items:
  #  tags = item['data']['tags']
  #  all_tags.extend([v for dic in tags for k,v in dic.items()])
  #print(all_tags)
  #return set(all_tags) # unique values only