let deleteBtns;
const listCheckboxes = document.querySelectorAll('.list-check-completed');
for (let i = 0; i < listCheckboxes.length; i++) {
    const checkbox = listCheckboxes[i];

    checkbox.onchange = function (e) {
        if (e.target.checked) {
            const listId = e.target.dataset.id;

            fetch('/lists/' + listId + '/set-completed', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(function (jsonResponse) {
                document.getElementById('error').className = 'hidden';

                const todoCheckboxes = document.querySelectorAll('.todo-check-completed');

                for (let i = 0; i < todoCheckboxes.length; i++) {
                    const checkbox = todoCheckboxes[i];

                    checkbox.checked = true;
                }
            })
            .catch(function () {
                document.getElementById('error').className = '';
            })
        }
    }
}


const todoCheckboxes = document.querySelectorAll('.todo-check-completed');
for (let i = 0; i < todoCheckboxes.length; i++) {
    const checkbox = todoCheckboxes[i];

    checkbox.onchange = function (e) {
        const newCompleted = e.target.checked;
        const todoId = e.target.dataset.id;

        fetch('/todos/' + todoId + '/set-completed', {
            method: 'POST',
            body: JSON.stringify({
                'completed': newCompleted
            }),
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(function (jsonResponse) {
            document.getElementById('error').className = 'hidden';
        })
        .catch(function () {
            document.getElementById('error').className = '';
        })
    }
}

deleteBtns = document.querySelectorAll(".delete-todo");

for (let i = 0; i < deleteBtns.length; i++) {
  const deleteBtn = deleteBtns[i];
  deleteBtn.onclick = function(e) {
    console.log("Delete event: ", e);
    const todoId = e.target.dataset.id;
    fetch('/todos/'+ todoId + '/delete',{
      method: 'DELETE'
    }).then(function() {
      console.log('Parent?', e.target);
      const item = e.target.parentElement;
      item.remove();
        document.getElementById("error").className = "hidden";
      })
      .catch(function(e) {
        console.error(e);
        document.getElementById("error").className = "";
      });
  };
}

deleteListBtns = document.querySelectorAll(".delete-list");

for (let i = 0; i < deleteListBtns.length; i++) {
  const deleteBtn = deleteListBtns[i];
  deleteBtn.onclick = function(e) {
    console.log("Delete event: ", e);
    const listId = e.target.dataset.id;

    fetch('/lists/'+ listId + '/delete',{
      method: 'DELETE'
    }).then(function() {
      console.log('Parent?', e.target);
      const item = e.target.parentElement;
      item.remove();
        document.getElementById("error").className = "hidden";
        window.location.reload(true);
      })
      .catch(function(e) {
        console.error(e);
        document.getElementById("error").className = "";
      });
  };
}


document.getElementById('todo-form').onsubmit = function (e) {
  e.preventDefault();

  fetch('/todos/create', {
      method: 'POST',
      body: JSON.stringify({
          'description': document.getElementById('description').value,
          'list_id': document.getElementById('list_id').value
      }),
      headers: {
          'Content-Type': 'application/json'
      }
  })
  .then(function (response) {
      return response.json();
  })
  .then(function (jsonResponse) {
      const liItem = document.createElement('LI');

      liItem.innerHTML = jsonResponse['description'];
      document.getElementById('todos').appendChild(liItem);
      document.getElementById('error').className = 'hidden';
      window.location.reload(true);
  })
  .catch(function () {
      document.getElementById('error').className = '';
  })
}

document.getElementById('list-form').onsubmit = function (e) {
  e.preventDefault();

  fetch('/lists/create', {
      method: 'POST',
      body: JSON.stringify({
          'name': document.getElementById('todolist-input').value
      }),
      headers: {
          'Content-Type': 'application/json'
      }
  })
  .then(function (response) {
      return response.json();
  })
  .then(function (jsonResponse) {
      const liItem = document.createElement('LI');

      liItem.innerHTML = jsonResponse['name'];
      document.getElementById('lists').appendChild(liItem);
      document.getElementById('error').className = 'hidden';
      window.location.reload(true);
  })
  .catch(function (err) {
      document.getElementById('error').className = '';
  })
}