function edit(anchor){
  const review = anchor.getAttribute('data-review');
  const rating = anchor.getAttribute('data-rating');
  const isbn = anchor.getAttribute('data-isbn');
  const title = anchor.getAttribute('data-title');
  const author = anchor.getAttribute('data-author');
  const year = anchor.getAttribute('data-year');

  book_data = document.querySelectorAll('.book-data');
  book_data[0].innerHTML = title;
  book_data[1].innerHTML = author;
  book_data[2].innerHTML = year;
  book_data[3].innerHTML = isbn;

  let book_list = document.getElementById('book-list');
  $("[data-toggle='tooltip']").tooltip('hide');
  book_list.innerHTML='';
   
  // const alert = document.querySelector('.alert');
  // alert.innerHTML = 'You can change both input fields and then submit it.'

  const form = document.getElementById('form-add-review');
  const edit_container = document.querySelector('.edit-container');
  const input_rating = document.querySelector('input[name="rating"]');
  const input_isbn = document.querySelector('input[name="isbn"]');
  const textarea = document.querySelector('textarea[name="review"]');

  input_rating.value = rating;
  input_isbn.value = isbn;
  textarea.value = review;

  edit_container.classList.remove('hide-block');
  edit_container.classList.add('show-block');
  form.classList.remove('hide-block');
  form.classList.add('show-block');
  input_rating.focus();
  // edit_container.style.marginTop = "-40px";

}