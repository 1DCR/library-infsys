document.getElementById('search-btn').addEventListener('click', function () {
    const title = document.getElementById('search-title').value.toLowerCase();
    const author = document.getElementById('search-author').value.toLowerCase();
    const genre = document.getElementById('search-genre').value;

    const books = document.querySelectorAll('.book-card');

    books.forEach(book => {
        const bookTitle = book.dataset.title.toLowerCase();
        const bookAuthor = book.dataset.author.toLowerCase();
        const bookGenre = book.dataset.genre;

        if (
            (title === '' || bookTitle.includes(title)) &&
            (author === '' || bookAuthor.includes(author)) &&
            (genre === '' || bookGenre === genre)
        ) {
            book.style.display = 'block';
        } else {
            book.style.display = 'none';
        }
    });
});