window.addEventListener('load', async () => {
    async function get_forum() {
        let response = await fetch(API_POST)
        return response.json()
    }


    function print_posts(posts){
        for (let post of posts) {
            forum_posts.innerHTML += `
                <div class="post">
                    <a href="/foro/post/${post.id}"><h3>${post.title}</h3></a>
                    <span class="views"><i class="fas fa-eye"></i><span class="amount">${post.views}</span></span>
                    <p class="date_post">${post.date}</p>
                    <p class="user_name"><a href="/usuario/perfil/${post.user_name}">${post.user_name}</a></p>
                </div>
                `
        }
    }


    const API_POST = "http://127.0.0.1:5001/api/foro"
    let forum_posts = document.getElementById('forum_posts')
    let create_post = document.getElementById('create_post')
    let add_post = document.getElementById('add_post')

    add_post.addEventListener('click', () => {
        window.location.href = "/foro/post/crear"
    })
    /************************Get all the posts**********************************/
    let response_post = await get_forum()
    console.log(response_post.response)
    if (localStorage.getItem('token')) {
        create_post.style.display = "block"
    }

    if (typeof response_post.response == "string") {
        forum_posts.innerHTML = `
        <div id="noPosts">
            <p>Por el momento no hay ningun post en el foro</p>
        </div>
        `
    } else {

        let all_posts = response_post.response.posts
        let aux = all_posts
        all_posts = all_posts.sort(function (a, b) { return b - a });

        for (let post of all_posts) {
            forum_posts.innerHTML += `
                <div class="post">
                    <a href="/foro/post/${post.id}"><h3>${post.title}</h3></a>
                    <span class="views"><i class="fas fa-eye"></i><span class="amount">${post.views}</span></span>
                    <p class="date_post">${post.date}</p>
                    <p class="user_name"><a href="/usuario/perfil/${post.user_name}">${post.user_name}</a></p>
                </div>
                `
        }



        /************************Order all the posts for views**********************************/
        let more_views = document.getElementById('more_views')
        let less_views = document.getElementById('less_views')
        let more_new = document.getElementById('more_new')
        let old = document.getElementById('old')
        let filters_class = document.getElementsByClassName('filter')
        console.log(filters_class)
        console.log(filters_class[0].classList.contains('push_button'))

        more_views.addEventListener('click', () => {
            more_views.classList.add('push_button')
            filters_class[1].classList.remove('push_button')
            filters_class[2].classList.remove('push_button')
            filters_class[3].classList.remove('push_button')

            let aux_more_views = aux
            forum_posts.innerHTML = ""
            aux_more_views.sort(function (a, b) { return b.views - a.views });
            for (let views_up of aux_more_views) {
                forum_posts.innerHTML += `
                <div class="post">
                    <a href="/foro/post/${views_up.id}"><h3>${views_up.title}</h3></a>
                    <span class="views"><i class="fas fa-eye"></i><span class="amount">${views_up.views}</span></span>
                    <p class="date_post">${views_up.date}</p>
                    <p class="user_name"><a href="/usuario/perfil/${views_up.user_name}">${views_up.user_name}</a></p>
                </div>
                `
            }
        })


        less_views.addEventListener('click', () => {
            less_views.classList.add('push_button')
            filters_class[0].classList.remove('push_button')
            filters_class[2].classList.remove('push_button')
            filters_class[3].classList.remove('push_button')

            let aux_less_views = aux
            forum_posts.innerHTML = ""
            aux_less_views.sort(function (a, b) { return a.views - b.views });
            for (let views_down of aux_less_views) {
                forum_posts.innerHTML += `
                <div class="post">
                    <a href="/foro/post/${views_down.id}"><h3>${views_down.title}</h3></a>
                    <span class="views"><i class="fas fa-eye"></i><span class="amount">${views_down.views}</span></span>
                    <p class="date_post">${views_down.date}</p>
                    <p class="user_name"><a href="/usuario/perfil/${views_down.user_name}">${views_down.user_name}</a></p>
                </div>
                `
            }
        })




        /************************Order all the posts for date**********************************/
        let objectPost = {
            "title": "",
            "description": "",
            "date": "",
            "user": "",
            "views": "",
            "id": "",
            "numberOrder": ""
        }
        let arrObjectPost = []

        let arrDate = []
        let time_post = []

        for (let date_post of all_posts) {
            arrDate.push(date_post.date)
        }

        for (let time of arrDate) {
            let aux = time.split(' ')
            time_post.push(aux)
        }

        let arrNumbers = []
        for (let number of time_post) {

            let days = number[0].split('-').join("")
            let hours = number[1].split(':').join("")
            let full_date = days + hours

            arrNumbers.push(full_date)
        }



        all_posts.forEach((element, index) => {
            arrObjectPost.push({
                "title": element.title,
                "description": element.description,
                "date": element.date,
                "user": element.user_name,
                "views": element.views,
                "id": element.id,
                "numberOrder": arrNumbers[index]
            })
        })



        more_new.addEventListener('click', () => {
            more_new.classList.add('push_button')
            filters_class[0].classList.remove('push_button')
            filters_class[1].classList.remove('push_button')
            filters_class[3].classList.remove('push_button')
            arrObjectPost.sort(function (a, b) { return b.numberOrder - a.numberOrder })
            forum_posts.innerHTML = " "
            for (let post of arrObjectPost) {
                forum_posts.innerHTML += `
            
            <div class="post">
                <a href="/foro/post/${post.id}"><h3>${post.title}</h3></a>
                <span class="views"><i class="fas fa-eye"></i><span class="amount">${post.views}</span></span>
                <p class="date_post">${post.date}</p>
                <p class="user_name"><a href="/usuario/perfil/${post.user_name}">${post.user}</a></p>
            </div>
            
            `
            }
        })


        old.addEventListener('click', () => {
            old.classList.add('push_button')
            filters_class[0].classList.remove('push_button')
            filters_class[1].classList.remove('push_button')
            filters_class[2].classList.remove('push_button')
            arrObjectPost.sort(function (a, b) { return a.numberOrder - b.numberOrder })
            forum_posts.innerHTML = " "
            for (let post of arrObjectPost) {
                forum_posts.innerHTML += `
            
            <div class="post">
                <a href="/foro/post/${post.id}"><h3>${post.title}</h3></a>
                <span class="views"><i class="fas fa-eye"></i><span class="amount">${post.views}</span></span>
                <p class="date_post">${post.date}</p>
                <p class="user_name"><a href="/usuario/perfil/${post.user_name}">${post.user}</a></p>
            </div>
            
            `
            }
        })

        /************************Search Posts**********************************/

        let search = document.getElementById('search_post')
        let arrLetters = []
        var arrSearch = []
        let searchWords = ""
        let auxArray = []
        let secondAux = []
        let found = false
        search.addEventListener('keydown', (event) => {
            if (event.key == "Backspace" || event.key == "Shift" || event.key == "CapsLock" ||
                event.key == "Control" || event.key == "Alt") {
                if (event.key == "Backspace") {

                    arrLetters.pop()
                    searchWords = arrLetters.join('')
                    if (auxArray.length == 0 && found) {
                        forum_posts.innerHTML = ""
                        print_posts(all_posts)
                    } else {
                        found = false
                        secondAux = auxArray
                        auxArray = []
                        all_posts.forEach(element => {
                            if (element.title.search(searchWords) != -1 || element.user_name.search(searchWords) != -1) {
                                auxArray.push(element)

                                found = true
                            }
                        })
                        if (auxArray.length == 0 && found) {
                            auxArray = secondAux
                        }
                        forum_posts.innerHTML = " "
                        print_posts(auxArray)
                    }
                }
            } else {
                arrLetters.push(event.key)
                searchWords = arrLetters.join('')

                secondAux = auxArray
                all_posts.forEach(element => {
                    if (element.title.search(searchWords) != -1 || element.user_name.search(searchWords) != -1) {
                        arrSearch.push(element)
                    }
                })
                forum_posts.innerHTML = " "
                print_posts(arrSearch)
                auxArray = arrSearch
                if (auxArray.length == 0) {
                    auxArray = secondAux
                }
                arrSearch = []

            }
        })

    }






})
