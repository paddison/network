document.addEventListener('DOMContentLoaded', () => {
    const editLinks = document.querySelectorAll('.edit');
    const likebuttons = document.querySelectorAll('.like-btn');

    editLinks.forEach(link => {
        link.addEventListener('click', editPost)
    });
    likebuttons.forEach(button => {
        button.addEventListener('click', likePost)
    })
});

function editPost() {
    const id = this.dataset.id
    const post = document.querySelector(`#post${id}`)
    post.firstElementChild.style.display = "none";
    post.lastElementChild.style.display = 'block';
    const text = document.querySelector(`#edit-field${id}`)

    document.querySelector(`#edit-btn${id}`).onclick = () => {
        fetch(`edit`, {
            method: 'PUT',
            body: JSON.stringify({
                id: id,
                text: text.value
            })
        })
        .then(response => response.json())
        .then(result => {
            text.value = result.text;
            text.dataset.original = result.text;
            post.firstElementChild.style.display = "block";
            post.lastElementChild.style.display = 'none';
            document.querySelector(`#text${id}`).innerHTML = result.text;
            return false;
        })
    }

    document.querySelector(`#cancel-btn${id}`).onclick = () => {
        text.value = text.dataset.original
        post.firstElementChild.style.display = "block";
        post.lastElementChild.style.display = 'none';
        return false;
    }
}

function likePost() { 
    const likeCounter = document.querySelector(`#like-count${this.dataset.id}`)
    fetch(window.location.origin + '/like', {
        method: 'POST',
        body: JSON.stringify({
            id: this.dataset.id,
            liked: this.dataset.liked
        })
    })
    .then(response => response.json())
    .then(result => {
        if (result.liked === true) {
            this.innerHTML = '<i class="fas fa-thumbs-up">';
            likeCounter.innerHTML = parseInt(likeCounter.innerHTML) + 1;
            return false;
        }else {
            this.innerHTML = '<i class="far fa-thumbs-up">';
            likeCounter.innerHTML = parseInt(likeCounter.innerHTML) - 1;
            return false;     
        }
    })
}