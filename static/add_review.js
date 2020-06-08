addEventListener('DOMContentLoaded', listeners);

function listeners(){
   
  let  add_review = document.getElementById('add-review');
  let  form_review = document.getElementById('form-add-review');

  add_review.addEventListener('click', show_hide_form);

  function show_hide_form(){
    if (form_review.classList.contains('hide-form')){
      form_review.classList.remove('hide-form');
      form_review.classList.add('show-form');
    }
    else {
      form_review.classList.remove('show-form');
      form_review.classList.add('hide-form');
    }
  }
   

}