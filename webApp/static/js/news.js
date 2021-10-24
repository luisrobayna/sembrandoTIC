window.addEventListener('load',async()=>{
    async function get_news(){
        let response = await fetch(API_NEWS)
        return response.json()
    }

    async function get_user(token){
        const response = await fetch(API_REST,{method:'GET',
        headers: {'Authorization': 'Bearer '+token}})
        return response.json()
    }



    const API_NEWS = "http://127.0.0.1:5001/api/noticias"
    const API_REST = "http://127.0.0.1:5001/api/verify/token"
    let main_news = document.getElementById('main_news')
    let secondary_news = document.getElementById('secondary_news')
    let button_create = document.getElementById('button_create')
    
    let news = await get_news()
    console.log(news.articles.length)
    if (news.articles.length == 0){
        main_news.innerHTML = `
        <div id="mssg_new">
            <p>Todavia no hay ninguna noticia publicada</p>
        </div>
        `
    }else{
        
    }

    news = news.articles.sort(function(a, b){return b - a});
    news.forEach((element,index)=>{
        if (index == 0){
            main_news.innerHTML= `
            <div id="main_new_info">
                <h2 class="title_new"><a href="/noticia/${element.id}">${element.title}</a></h2>
                <p class="date"><span>${element.date}</span></p>
                <p class="description_new">${element.description}</p>
            </div>
            <div id="main_new_image">
                <img src="/static/img/img_web/${element.image}" alt="${element.description}">
            </div>
            `
        }else{
            secondary_news.innerHTML+= `
            <div class="new">
                <img src="/static/img/img_web/${element.image}" alt="${element.description}">
                <h3 class="title_new"><a href="/noticia/${element.id}">${element.title}</a></h3>
            </div>
            `
        }
    })

    if (localStorage.getItem('token')){
        let user = await get_user(localStorage.getItem('token'))
        if (user.user_name == "adminMaster01" || user.user_name == "adminMaster02"){
            button_create.classList.add('button_class')
        }
    }

    

})