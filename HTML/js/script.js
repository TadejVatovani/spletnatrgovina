window.onload = function(){
  init();
}

function init(){
	var categories=document.getElementById("categories").children;
	for(var i=0;i<categories.length;i++){
		document.getElementById(categories[i].id).addEventListener("click", function(){	
			var items= [];
			for(var i=0;i<10;i++){
				var ele={
					name:this.id,
					path:"./izdelki/zmaj.jpg",
					price:10.01				
				};	
				items.push(ele);
			}
			var e = document.getElementById("items");
			e.innerHTML="";
			for(var i=0;i<items.length;i++){
			var ele=items[i];
			e.innerHTML+="<div style=\"min-width: 200px;max-width:300px; margin: 0px 20px 20px 20px;\"><img src=\""+ele.path
						+"\" style=\"width:100%;height:auto;\"></img><div style=\"font-weight:bold;\">"
						+ele.name+" "+ele.price+"€</div></div>";
			}
		});
	}
}

