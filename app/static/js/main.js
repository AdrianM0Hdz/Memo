const button = document.querySelector('#show-answer');

button.addEventListener('click', (event) => {
    const ans = document.querySelector('#definition');
    if (ans.style.display == 'block') {
        ans.style.display = 'none';
        button.innerHTML = 'SHOW ANSWER';
    } else {
        ans.style.display = 'block';
        button.innerHTML = 'HIDE ANSWER';
    }
})