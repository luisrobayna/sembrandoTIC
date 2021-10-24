window.addEventListener('load', async()=>{
    
    async function get_last_news(){
        let response = await fetch(API_NEWS)
        return response.json()
    }

    async function get_last_posts(){
        let response = await fetch(API_FORO)
        return response.json()
    }

    const API_NEWS = "http://127.0.0.1:5001/api/noticias"
    const API_FORO = "http://127.0.0.1:5001/api/foro"
    
    let news = document.getElementById('news')
    let last_news = await get_last_news()
    console.log(last_news.articles.length)
    if(last_news.articles.length == 0){
        
    }else{
        if(last_news.articles.length >= 3){
            last_news = last_news.articles.sort(function(a, b){return b - a});
    
            last_news.forEach((element ,index)=>{
                if (index <= 2){
                    news.innerHTML+=`
                    <div class="card_news">
                    <img src="/static/img/img_web/${element.image}" alt="${element.description}">
                        <a href="/noticia/${element.id}">
                            <h3>${element.title}</h3>
                        </a>
                    </div>
                    `
                }
            })
        }
        
    }
    

    let posts = document.getElementById('center')
    let last_posts = await get_last_posts()
    console.log(last_posts.response)
    if (typeof last_posts.response == "string"){
        posts.innerHTML = ""
    }else{
        if(last_posts.response.posts.length >= 3){
            last_posts = last_posts.response.posts.sort(function(a, b){return b - a});
    
            last_posts.forEach((element ,index)=>{
                if (index <= 2){
                    posts.innerHTML+=`
                    <div class="card_forum">
                    <a href="/foro/post/${element.id}">
                        <h3>${element.title}</h3>
                    </a>
                    <p>${element.description}</p>
                </div>
                    `
                }
            })
        }
        
    }
    



  

    
    


})