addEventListener('DOMContentLoaded', listeners);

function listeners(){
   
  let book_list = document.getElementById('book-list');
  let input = document.querySelector('#search-input');
  let alert = document.querySelector('.alert');
  let form = document.querySelector('.form-boot');
  let container = document.querySelector('.edit-container');

  input.addEventListener('change', search_clean);
  input.addEventListener('keyup', search_clean);
  input.addEventListener('paste', search_clean);

  function search_clean(){
    book_list.innerHTML = '';
    alert.style.display = "none";
    form.style.display = 'none';
    container.style.display = 'none';
    // remove event listeners
    input.removeEventListener('change', search_clean);
    input.removeEventListener('keyup', search_clean);
    input.removeEventListener('paste', search_clean);
  }
}