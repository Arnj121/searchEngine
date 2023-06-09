var searching=0

document.getElementById('searchInput').addEventListener('keydown',(e)=>{
    if(e.key === 'Enter'){
        document.getElementById('submit').click()
    }
})
var scontroller=0,scounter=0
function watcher(){
    if (searching===1){
        scontroller = setInterval(()=>{
            var scc = ''
            for (let i=0;i<=scounter;i++){
                scc+='.'
            }
            scounter=scounter+1
            scounter=scounter%3
            document.getElementById('searching').innerText = 'Searching'+scc
        },500)
        document.getElementById('searching').style.visibility='visible'
    }
    else{
        clearInterval(scontroller)
        document.getElementById('searching').style.visibility='hidden'
    }
}
var pages={0:{}}
var currentPage=0
function Filter(data){
    let cp=0,cn=0;
    for(let i of Object.keys(data)){
        if (parseFloat(data[i][0]) > 0) {
            pages[0][cp] = data[i]
            cp += 1
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
    console.log(v)
    await Filter(v)
    tot=Object.keys(pages[0]).length
    const timeend = performance.now()
    time=Math.round((timeend-timest)*1000)/1000000
    document.getElementById('results').innerText=''
    // showPageNo()
    displayTime()
    displayPage(0)
    searching=0
    watcher()
}

function displayTime(){
    let cv = document.createElement('label')
    cv.style.borderRadius='50px'
    cv.style.color='#F57F17'
    cv.style.border = '1px #90A4AE solid'
    cv.style.padding= '5px 10px'
    cv.innerText=`About ${tot} results (${time}s)`
    cv.style.margin = '5px'
    document.getElementById('results').appendChild(cv)
}
function displayPage(pageNo){
    let v = pages[pageNo]
    for( let i of Object.keys(v)){
        let div = document.createElement('div')
        div.className='searchClass'
        let content = document.createElement('a')
        let lnk = document.createElement('p')
        let cos = document.createElement('label')
        let perc=v[i][0]*100
        cos.innerText='match score = '+ String(perc).slice(0,5) + '%'
        cos.style.color='whitesmoke'
        content.style.color='whitesmoke'
        content.href=v[i][1]
        content.innerText=v[i][2].substr(0,100)
        content.style.overflowWrap='break-word'
        content.target = '_blank'
        content.style.textDecoration='none'
        lnk.style.color='#FF3D00'
        lnk.style.textDecoration='underline'
        lnk.style.fontSize='small'
        lnk.innerText = v[i][1]
        // content.style.lineBreak='anywhere'
        // match.innerText =`score - ${Math.round(v[i][0]*100)/100}`
        div.append(content,lnk,cos)
        document.getElementById('results').appendChild(div)
    }
}

function showPageNo(){
    let l = document.createElement('div')
    let lbl = document.createElement('label')
    lbl.innerText='Page'
    l.append(lbl)
    l.id='pageList'
    for(let i of Object.keys(pages)){
        let p = document.createElement('label')
        p.innerText = parseInt(i)+1
        p.className='pagelinks'
        p.id=`pageNo${i}`
        p.addEventListener('click',(e)=>{
            let k=document.getElementById(e.target.id).innerText
            document.getElementById('results').innerText=''
            showPageNo()
            displayTime()
            displayPage(parseInt(k)-1)
            document.getElementById(`pageNo${currentPage}`).style.background='white'
            currentPage=parseInt(k)-1
            document.getElementById(`pageNo${currentPage}`).style.background='#B0BEC5'
        })
        l.appendChild(p)
    }
    document.getElementById('results').append(l)
    document.getElementById(`pageNo${currentPage}`).style.background='#B0BEC5'
}