document.addEventListener('DOMContentLoaded', function(){  
    const submit = document.querySelector('#submit');
    const captionform  = document.querySelector('#captionform');
    const followbutton = document.querySelector('#followbutton');
    const postform = document.querySelector('#postform');
    const posts = document.querySelectorAll('[id=post]');
    const likebtn = document.querySelectorAll('[id=likebutton]');    
    const likecnt = document.querySelectorAll('[id=likecount]');   
    if (followbutton != null)
    {
        get_status(followbutton.value);
        
        followbutton.addEventListener("click", function() {    
            let str = '/follow_user/'
            id = followbutton.value.toString();
            fetch(str += id, {
                method: 'POST'
            })
            .then(response => response.json())
            .then(data => {
                console.log(data);
                get_status(followbutton.value);
            })
            .catch((error) => {
                console.error('Error:', error);
            });
        });
    }
    
    if (likebtn != null)
    {
        for (let i = 0; i < likebtn.length; i++)
        {
            _id = likebtn[i].dataset.id.toString();
            is_liked(_id, likebtn[i],likecnt[i]);
            likebtn[i].addEventListener("click", function() { 
                let str = '/like_post/'
                _id = likebtn[i].dataset.id.toString();
                fetch(str += _id, {
                    method: 'POST'
                })
                .then(response => response.json())
                .then(data => {
                    console.log(data);
                    is_liked(_id, likebtn[i],likecnt[i]);
                })
                .catch((error) => {
                    console.error('Error:', error);
                });
            })
        }
    }

    if (posts != null)
    {
        const editdiv = document.querySelectorAll('#editdiv'); 
        const editarea = document.querySelectorAll('#editarea');
        const contentarea = document.querySelectorAll('#contentarea');
        const submitedits = document.querySelectorAll('#submitedit');
        
        for (let i = 0; i < posts.length; i++) {
            post_id = posts[i].dataset.id;
            let str = '/is_mypost/'
            id = post_id.toString();
            fetch(str += id, {
                method: 'POST'
            })
            .then(response => response.json())
            .then(data => {
                let edit_button = editdiv[i];
                if (data["result"] == 'success')
                {
                    
                    edit_button.addEventListener("click", function() {  
                        editarea[i].querySelector('#txtid').value = contentarea[i].querySelector('.post__headerDescription p').innerHTML;
                        let submitedit = posts[i].querySelector("#submitedit");
                        let to_hide = posts[i].querySelector(".post__footer");
                        
                        editarea[i].style.display = 'block';
                        contentarea[i].style.display = 'none';
                        to_hide.style.display = 'none';
                        submitedit.style.display = 'table';
                        edit_button.style.display = 'none';

                        submitedit.addEventListener("click", function() {
                            let editurl = '/edit_post/';
                            let postId = submitedit.dataset.id.toString();
                            fetch(editurl += postId, {
                                    method: 'POST',
                                    body: JSON.stringify({
                                        caption: editarea[i].querySelector('#txtid').value
                                    })
                                })
                                .then(response => response.json())
                                .then(result => {
                                  console.log(result);
                                  contentarea[i].style.display = 'block';
                                  contentarea[i].querySelector('.post__headerDescription p').innerHTML = editarea[i].querySelector('#txtid').value;
                                  editarea[i].style.display = 'none';
                                  
                                  to_hide.style.display = 'flex';
                                  submitedit.style.display = 'none';

                                  edit_button.style.display = 'inline-block';
                            });
                        });
                    });
                }
                else
                {
                    edit_button.style.display = 'none';
                }
            })
            .catch((error) => {
                console.error('Error:', error);
            });
        }
    }

    if(submit != null)
    {
        submit.disabled = true;
    
        captionform.onkeyup = () => {
            if (captionform.value.length > 0) {
                submit.disabled = false;
            }
            else {
                submit.disabled = true;
            }
        }
    }
    
    if (postform != null)
    {
        postform.onsubmit = () => {
            fetch('/add_post', {
                method: 'POST',
                body: JSON.stringify({
                    caption: captionform.value
                })
              })
              .then(response => response.json())
              .then(result => {
                console.log(result);
                window.location.href = window.location.href;
            });
            
            captionform.value = '';
            
            // Disable the submit button again:
            submit.disabled = true;
            
            // Stop form from submitting
            return false;
        }
    }
});

function get_status(id) {
    let str = '/follow_status/';
    id = id.toString();
    fetch(str += id, {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        if (data["result"] == 'success')
        {
            followbutton.innerHTML = "Unfollow";
            followbutton.style.backgroundColor='rgb(29, 161, 242)';
            followbutton.style.color='white';
        }
        else
        {
            followbutton.innerHTML = "Follow";
            followbutton.style.backgroundColor='transparent';
            followbutton.style.color='rgb(29, 161, 242)';
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

function is_liked(_id, x, y) {
    let _str = '/is_liked/';
    _id = _id.toString();
    fetch(_str += _id, {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        if (data["result"] == 'success')
        {
            x.innerHTML = "favorite";
        }
        else
        {
            x.innerHTML = "favorite_border";
        }

        y.innerHTML = data["likecount"]
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}