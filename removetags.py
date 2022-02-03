from pyzotero import zotero
import secrets # Api key and ID from secrets.py

# Split list into chunks of n items
def chunks(l,n):
  for i in range(0, len(l), n):
    yield l[i:i+n]
    
# Make Zotero connection
library_id = secrets.library_id
api_key = secrets.api_key
library_type = 'user'
zot = zotero.Zotero(library_id, library_type, api_key)

# Testing
#all_tags = []
#items = zot.top(limit=5)
#for item in items:
#  tags = item['data']['tags']
#  all_tags.extend([v for dic in tags for k,v in dic.items()])
#print(all_tags)
#all_tags = set(all_tags) # unique values only

# Grab all tags and return all articles for a tag
# That the search is not case-sensitive!
# Add tags with only one article to-be-deleted list
deleted_tags = []
all_tags = zot.everything(zot.tags())
for t in all_tags:
  zot.add_parameters(tag=t) # Search by tag
  tag_items = zot.items()
  n_items = len(tag_items)
  print(f'tag:{t} n:{n_items}')
  if n_items == 1:
    deleted_tags.append(t)
    print(f'\t Assined for deletion:')
# Write all tags to a file 
print('Writing tags to file')
with open('deletetags.txt','w') as f:
  for t in deleted_tags:
    f.write('%s\n' % t)

# Delete tags
print(f'Deleting tags: {deleted_tags}')
# If more than 50 then we need to do a loopy loop
if len(deleted_tags) > 50:
  chunked = list(chunks(deleted_tags, 50)) # Split list
  for l in chunked:
    zot.delete_tags(*l)
else:
  zot.delete_tags(*deleted_tags)
n_tags = len(deleted_tags)
print(f'Deleted {n_tags} tags.')