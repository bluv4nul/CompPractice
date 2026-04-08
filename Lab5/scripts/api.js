const URL = "https://api.thecatapi.com/v1/images/search"

async function getKitten() {
    const response = await ( await fetch(URL)).json()
    return response[0].url
}

document.getElementById('bt').addEventListener('click', async () => {  
    const url = await getKitten()
    window.open(url)
})