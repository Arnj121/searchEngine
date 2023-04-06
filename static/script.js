var searching=0

document.getElementById('searchInput').addEventListener('keydown',(e)=>{
    if(e.key === 'Enter'){
        document.getElementById('submit').click()
    }
})
function watcher(){
    if (searching===1){
        document.getElementById('searching').style.visibility='visible'
    }
    else{
        document.getElementById('searching').style.visibility='hidden'
    }
}
var pages={0:{},1:{}}
var currentPage=0
function Filter(data){
    let cp=0,cn=0;
    for(let i of Object.keys(data)){
        if (parseFloat(data[i][0]) > 0) {
            pages[0][cp] = data[i]
            cp+=1
        }
        else {
            pages[1][cn] = data[i]
            cn+=1
        }
    }
}
var time=0,tot=0
async function search(){
    searching=1
    watcher()
    const timest = performance.now()
    const res = await fetch(`http://127.0.0.1:5000/search?q=${document.getElementById('searchInput').value}`)
    const v = await res.json()
    tot=Object.keys(v).length
    await Filter(v)
    const timeend = performance.now()
    time=Math.round((timeend-timest)*1000)/1000000
    document.getElementById('results').innerText=''
    displayTime()
    displayPage(0)
    showPageNo()
    searching=0
    watcher()
}

function displayTime(){
    let cv = document.createElement('label')
    cv.innerText=`About ${tot} results (${time}s)`
    cv.style.margin = '5px'
    document.getElementById('results').appendChild(cv)
}
function displayPage(pageNo){
    let v = pages[pageNo]
    for( let i of Object.keys(v)){
        let div = document.createElement('div')
        div.className='searchClass'
        let lnk = document.createElement('a')
        let content = document.createElement('p')
        let match = document.createElement('label')
        lnk.href=v[i][1]
        lnk.innerText=v[i][1]
        lnk.target = '_blank'
        content.innerText = v[i][2].substr(0,100)
        content.style.lineBreak='anywhere'
        match.innerText =`Match rank - ${Math.round(v[i][0]*100)/100}`
        div.append(match,lnk,content)
        document.getElementById('results').appendChild(div)
    }
}

function showPageNo(){
    let l = document.createElement('div')
    l.id='pageList'
    for(let i of Object.keys(pages)){
        let p = document.createElement('label')
        p.innerText = parseInt(i)+1
        p.className='pagelinks'
        p.id=`pageNo${i}`
        p.addEventListener('click',(e)=>{
            let k=document.getElementById(e.target.id).innerText
            document.getElementById('results').innerText=''
            displayTime()
            displayPage(parseInt(k)-1)
            showPageNo()
            document.getElementById(`pageNo${currentPage}`).style.textDecoration='none'
            currentPage=parseInt(k)-1
            document.getElementById(`pageNo${currentPage}`).style.textDecoration='underline'
        })
        l.appendChild(p)
    }
    document.getElementById('results').append(l)
    document.getElementById(`pageNo${currentPage}`).style.textDecoration='underline'
}