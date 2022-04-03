# state-of-indices

Index names consist of 2 parts, the content type that is indexed and the timestamp that indicates the creation time of the index. The index "media-1641833637" means that the content type is “media”, 1641833637 in the name of the index is a unix timestamp which gives us the information that the index was created on the 10th of January at 16:53 GMT.
The index "media-1641833637" has next aliases:
[ {"alias": "media--read", "index": "media-1641833637", "is_write_index": "false"},
{"alias": "media--write", "index": "media-1641833637", "is_write_index": "true"}]
Required data:
- Age of indices
- Number of documents in each index
- Flag indices that have both read and write aliases


## How to run