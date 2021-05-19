function getHeight(expandable){
	let expand=expandable.getElementsByClassName("expand")[0];
	expand.style.setProperty("--max-height",expand.scrollHeight+"px");
}

function show(event){
  let elmnt=event.target;
  event.stopPropagation();
	let expandable=elmnt.closest(".expandable");
  getHeight(expandable);
	expandable.classList.toggle("selected");
}

for(item of document.querySelectorAll("a,button,input,textarea,select,.expand")){
	item.onclick=()=>event.stopPropagation();
}

for(item of document.getElementsByClassName("expandable")){
	item.onclick=()=>show(event);
	if(item.classList.contains("selected")){getHeight(item);}
}

var urlString=location.href;
var url=new URL(urlString);
var selected=url.searchParams.get("selected");

if(selected!=null){
  console.log(selected);
	for(item of document.querySelectorAll(`div.expandable[name=${selected.toLowerCase().replace(/ /g,"-")}]`)){
		item.click();
    item.ontransitionend=function(){
      item.scrollIntoView();
      item.ontransitionend=undefined;
    }
	}
}