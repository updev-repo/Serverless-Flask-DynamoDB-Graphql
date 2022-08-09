const weekday = ["Sun","Mon","Tue","Wed","Thu","Fri","Sat"];
const months = [
  'Jan',
  'Feb',
  'Mar',
  'Apr',
  'May',
  'June',
  'July',
  'Aug',
  'Sep',
  'Oct',
  'Nov',
  'Dec',
]

const todo_div = document.querySelector(".ul")
const login_links = document.querySelectorAll("a")
const h1 = document.querySelector("h1")
let username = ""
let password = ""
document.querySelector(".logout-div").style.display = "none"

fetch('/graphql', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        query:`query GetAllTodo {
            allTodo{
                  id
                  description
                  dueDate
                  completed
            }
          }
          `,
    }),
})
.then((res) => res.json()
.then((result) => {
  console.log(result)
    data = result.data.allTodo
    data.forEach(item => {
      let mydate = new Date(item.dueDate)      
      let day = weekday[mydate.getDay()]
      let month = months[mydate.getMonth()]
      new_date = `${day} ${month} ${mydate.getDay()} ${mydate.getFullYear()}`
     
      todo_div.innerHTML += `
            <div class="desc">

            <li><h3>${item.description}</h3>
                <li>Due: ${new_date}</li>
                <li>Completed: ${item.completed ?     
                 `<input type="checkbox" checked="checked" disabled>` : `<input type="checkbox" disabled>`}</li>

            </li>
            <hr>
            </div>`
         
    });
    
}))

login_links.forEach(login_link => {
  login_link.addEventListener('click', (e) => {
    e.preventDefault()
    // Create login page
    console.log(e.target.className)
    if (e.target.className === "login"){
      h1.innerHTML = "Login"
      todo_div.innerHTML = `</div>
      <form method="post">
        <div class="mb-3">
          <label for="name" class="form-label">Name</label>
          <input type="name" name="username" class="form-control" id="username" aria-describedby="username">
        </div>
        <div class="mb-3">
          <label for="password" class="form-label">Password</label>
          <input type="password" name="password" class="form-control" id="password">
        </div>
        <div class="error-div"></div>
        <button type="button" class="login_btn btn btn-primary">Submit</button>
      </form>
      <div>`
      
      // Function gets the form item and store in order to fetch 
      // login endpoint
      function print_param() {
        console.log(document.querySelectorAll("form").
        forEach(el => {
            username = String(el.username.value)
            password = String(el.password.value)
        }))
        return username, password

      }
      
      const login_btn = document.querySelector(".login_btn")
      login_btn.addEventListener('click', () => {
      print_param()
      getLogin()
      console.log('clicked')
    
    })
      
    }
    if (e.target.className === "logout") {
      h1.innerHTML = ""
      todo_div.innerHTML = `<div style="text-align: center; margin-top: 5em;">
                            <h1>Logged Out</h1>
                            <h3>Bye for now</h3></div>`
      document.querySelector(".logout-div").style.display = "none";

    }
    if (e.target.className === "register") {
        h1.innerHTML = "Register"
        todo_div.innerHTML = `</div>
        <form method="post">
          <div class="mb-3">
            <label for="username" class="form-label">Name</label>
            <input type="name" name="username" class="form-control" id="username" aria-describedby="username">
          </div>
          <div class="mb-3">
            <label for="password" class="form-label">Password</label>
            <input type="password" name="password" class="form-control" id="password">
          </div>
          <div class="error-div"></div>

          <button type="button" class="register_btn btn btn-primary">Submit</button>
        </form>`

        function print_param() {
          console.log(document.querySelectorAll("form").
          forEach(el => {

              username = String(el.username.value)
              password = String(el.password.value)
          }))
          return username, password
  
        }

        const register_btn = document.querySelector(".register_btn")
        register_btn.addEventListener('click', () => {
        print_param()
        registerUser()
        console.log('clicked')})

      }
    
  
  })
  
})


function getLogin() {
  const query = `mutation loginAuth($name: String, $password: String ) {
    auth(name: $name, password: $password) {
        accessToken
        refreshToken
    }
  }
  `
  const variables = {name: username, password: password}


  fetch('/graphql', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({query, variables}),
  },)
  .then((res) => res.json()
  .then(result => {
    if (result.errors || result.data.auth == null) {
      document.querySelector(".error-div").innerHTML = "Invalid Username or Password"
      const error_msg = "Authenication Failure : User is not registered"
      result.errors.forEach(er => {
          if (er.message === error_msg || result.data.auth == 'null') {
            console.log(er.message)
            document.querySelector(".error-div").innerHTML = "Invalid Username or Password"
          }
          else {console.log("An error occured. Please try again")}
      })
    }
        else {
          h1.innerHTML = `Welcome`
          todo_div.innerHTML = `<div style="text-align: center; margin-top:5em;">
                                <h3>You are logged in as: <b> ${username}</h3></div>`
          document.querySelector(".reg-div").style.display = 'none'
          document.querySelector('.login-div').style.display = 'none'
          document.querySelector(".logout-div").style.display = "block";
    
    }

  }))
  
}

function registerUser() {
  const query = `mutation createUser($name: String, $password: String) {
    createUser(name: $name, password: $password) {
      user{
        name
        password
      }
    }   
  }`
  
  
  const variables = {name: username, password: password}

fetch('/graphql', {
  method: 'POST',
  headers: {
      'Content-Type': 'application/json'
  },
  body: JSON.stringify({query, variables
  }),
})
.then((res) => res.json()
.then((result) => {
  console.log(result.errors)
  if (result.errors) {
    const error_msg = "Name not available."
    result.errors.forEach(er => {
      if (er.message === error_msg) {
        console.log(er.message)
        document.querySelector(".error-div").innerHTML = error_msg
      }
      else {console.log("An error occured. Please try again")}
  })
  }
  else {
    h1.innerHTML = "Registration success"
    todo_div.innerHTML = "Proceed to login page. "
    document.querySelector(".reg-div").style.display = 'none'
    document.querySelector('.login-div').style.display = 'none'
    document.querySelector(".logout-div").style.display = "none";

  }
  
}))
}