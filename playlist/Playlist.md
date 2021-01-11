# Playlist
### How it works

`playlists` are saved on your computer in JSON format, which is easy to deal with.  
The JSON structure used by `WishTify` is very simple, it only stores the location of the songs in the list.

### Example stucture

Here is a short example of a basic JSON `playlist` file :
```json
{
    "list" : [
        "location/of/first/song.mp3",
        "location/of/second/song.mp3"
    ]
}
```

### Pros and Cons
Pros :  
`+` Easy to deal with  
`+` Human-readable  
`+` Commonly used for small amout of r/w  
  
Cons :  
`-` Path aren't relative (you can't share playlists with friends)  
`-` Lots of playlists = lots of JSON Files = lots of searching