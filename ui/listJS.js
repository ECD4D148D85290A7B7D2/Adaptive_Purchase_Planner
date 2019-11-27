function getData(time, userId){
    var xhttp = new XMLHttpRequest();
    var recommendations;
    xhttp.open("GET", "https://adaptivejames.azurewebsites.net/recommendations/" + time + "?user_id=" + userId, true);
    xhttp.send();
    xhttp.onreadystatechange = function(){
        if(this.readyState == 4 && this.status == 200){
            recommendations = JSON.parse(this.responseText);
            createList(recommendations, time, userId);
        }
    }
}
function getStereotypeRecs(userId){
    var stereoReq = new XMLHttpRequest();
    stereoReq.open("GET", "https://adaptivejames.azurewebsites.net/recommendations/stereo/predict?user_id=" + userId, true)
    stereoReq.send();
    stereoReq.onreadystatechange = function(){
        if(this.readyState == 4 && this.status == 200){
            var stereotypeRecs = JSON.parse(this.responseText);
            addStereoRec(stereotypeRecs);              
        }
    }
}
function getUserModel(userId){
    var userModel = new XMLHttpRequest();
    userModel.open("GET", "https://adaptivejames.azurewebsites.net/usermodel/view?user_id=" + userId, true)
    userModel.send();
    userModel.onreadystatechange = function(){
        if(this.readyState == 4 && this.status == 200){
            var userModel = JSON.parse(this.responseText); 
            createUserModelPage(userModel);
                  
        }
    }
}

function createUserModelPage(userModel){
    var i;
    for(i in userModel.userPurchaseModelAlgorithmic){
        var obj = userModel.userPurchaseModelAlgorithmic[i];
        var tr = document.createElement("tr");
        var itemCol = createListCol(obj.Product_Name);
        var sizeCol = createListCol(obj.Size);
        var freqCol = createListCol(obj.Purchase_Freq);
        tr.appendChild(itemCol);
        tr.appendChild(sizeCol);
        tr.appendChild(freqCol);
        document.getElementById("algoListBody").appendChild(tr);
        
    }
    for(i in userModel.userPurchaseModelML){
        var obj = userModel.userPurchaseModelML[i];
        var tr = document.createElement("tr");
        var itemCol = createListCol(obj.Product);
        var sizeCol = createListCol(obj.Size);
        var freqCol = createListCol(obj["Learned Frequencies"]);
        tr.appendChild(itemCol);
        tr.appendChild(sizeCol);
        tr.appendChild(freqCol);
        document.getElementById("mlListBody").appendChild(tr);
        
    }
}
function createList(json, time, userId){
    var i;
    for(i in json.data){
        var obj = json.data[i];
        var tr = document.createElement("tr");
        var idCol = createListCol(obj.Product);
        var itemCol = createListCol(obj.Product_Name);
        var sizeCol = createListCol(obj.Size);
        var priceCol = createListCol("€" + Math.round(obj.Approx_Item_Price*100)/100);
        tr.appendChild(idCol);
        tr.appendChild(itemCol);
        tr.appendChild(sizeCol);
        tr.appendChild(priceCol);
        if(time == "later"){
            var daysLeftCol = createListCol(obj.Days_Left);
            tr.appendChild(daysLeftCol);
        }
        else if(time =="ignored"){
            var ignoreButton = createIgnoreButton();
            tr.appendChild(ignoreButton);
            var close = document.getElementsByClassName("close");
            var i;
            for (i = 0; i < close.length; i++) {
                close[i].onclick = function() {
                    var div = this.parentElement;
                    div.classList.add("ignored");
                    submit("ignored", userId);
                    div.parentElement.removeChild(div);
                }
            }
        }
        document.getElementById("listBody").appendChild(tr);
    }
    addCheckboxEventListeners("notNow", "ignored", "notInterested");
    addCheckboxEventListeners("notInterested", "rejected", "notNow");
    addRowEventListener();

}
function addStereoRec(json){
    var i;
    for(i in json.data){
        var obj = json.data[i];
        var tr = document.createElement("tr");
        var idCol = createListCol(obj.product);
        var itemCol = createListCol(obj.name);
        tr.appendChild(idCol);
        tr.appendChild(itemCol);
        document.getElementById("listBody").appendChild(tr);
    }
    addCheckboxEventListeners("notNow", "ignored", "notInterested");
    addCheckboxEventListeners("notInterested", "rejected", "notNow");
}
function createListCheckbox(name){
    var tableCol = document.createElement("th");
    var checkbox = document.createElement("input");
    checkbox.setAttribute("type", "checkbox");
    checkbox.setAttribute("class", name);
    tableCol.appendChild(checkbox);
    return tableCol;
}
function createListCol(value){
    var thing = document.createElement("th");
    var textNode = document.createTextNode(value);
    thing.appendChild(textNode);
    return thing;
}
function createIgnoreButton(){
    var span = document.createElement("th");
    var txt = document.createTextNode("\u00D7");
    span.className = "close";
    span.appendChild(txt);
    return span;
}
function addCheckboxEventListeners(className, rowClass){
    var checkboxList = document.getElementsByClassName(className);
    var i;
    for(i=0;i<checkboxList.length;i++){
        checkboxList[i].addEventListener('click', function(ev){
            if(ev.target.tagName === "INPUT"){
                rowClasses = ev.target.parentElement.parentElement.classList;
                if(rowClasses.length == 0 || rowClasses.contains(rowClass)){
                    ev.target.parentElement.parentElement.classList.toggle(rowClass);
                }
            }
        }, false);
    }

}
function addRowEventListener(){
    var list = document.getElementById('list');
    list.addEventListener('click', function(ev) {
    if(ev.target.tagName === 'TH'){
        var rowClasses = ev.target.parentElement.classList
        ev.target.parentElement.classList.toggle('bought');
            
        
    }
    },false);
}
function submit(type, userId){
    var items = document.getElementsByClassName(type);
    var i;
    for(i = 0; i < items.length;i++){
        var productId = items[i].childNodes[0].innerText;
        //var itemName = items[i].childNodes[1].innerText;
        var itemSize = items[i].childNodes[2].innerText;
        //var itemPrice = items[i].childNodes[3].innerText;
        var request = new XMLHttpRequest();
        if(type == "bought"){
            request.open("POST", "https://adaptivejames.azurewebsites.net/purchase?user_id=" +userId + "&product_id=" + productId +"&size=" + itemSize+"&store=Aldi", true);
        }
        else if(type == "ignored"){
            request.open("POST", "https://adaptivejames.azurewebsites.net/usermodel/update?user_id=" +userId + "&product_id=" + productId +"&size=" + itemSize, true);
        }
        request.send();
    }
    var regen = new XMLHttpRequest();
    regen.open("GET", "https://adaptivejames.azurewebsites.net/regen/bond")
    regen.send();
    regen.onreadystatechange = function(){
        console.log(this.responseText);
    }
}
//ALL OF THIS BELOW IS FOR NEW ROW ADDITION AND  SUBMISSION
function createNewListItem(){
    var tr = document.createElement("tr");
    tr.setAttribute("id", "inputRow");
    var idCol = createListInput("ProductId");
    var itemCol = createListInput("Name");
    var sizeCol = createListInput("Size");
    var priceCol = createListInput("Price");
    var submitCol = createListSubmit();
    var cancelCol = createListCancel();
    tr.appendChild(idCol);
    tr.appendChild(itemCol);
    tr.appendChild(sizeCol);
    tr.appendChild(priceCol);
    tr.appendChild(submitCol);
    tr.appendChild(cancelCol);
    document.getElementById("listBody").appendChild(tr);
}
function createListSubmit(){
    var col = document.createElement("th");
    var button = document.createElement("button");
    var textNode = document.createTextNode("Add");
    button.appendChild(textNode);
    button.setAttribute("onClick", "submitNewRow()");
    col.appendChild(button)
    return col;
}
function createListCancel(){
    var col = document.createElement("th");
    var button = document.createElement("button");
    var textNode = document.createTextNode("Cancel");
    button.appendChild(textNode);
    button.setAttribute("onClick", "cancelNewRow()");
    col.appendChild(button)
    return col;
}
function cancelNewRow(){
    var input = document.getElementById("inputRow");
    input.parentNode.removeChild(input);
    
}
function createListInput(name){
    var tableCol = document.createElement("th");
    var checkbox = document.createElement("input");
    checkbox.setAttribute("type", "text");
    checkbox.setAttribute("id", name);
    tableCol.appendChild(checkbox);
    return tableCol;
}
function submitNewRow(){
    var input = document.getElementById("inputRow");
    var productId = document.getElementById("ProductId").value;
    var name = document.getElementById("Name").value;
    var size = document.getElementById("Size").value;
    var price = document.getElementById("Price").value;

    var tr = document.createElement("tr");
    var idCol = createListCol(productId);
    var itemCol = createListCol(name);
    var sizeCol = createListCol(size);
    var priceCol = createListCol(price);
    tr.appendChild(idCol);
    tr.appendChild(itemCol);
    tr.appendChild(sizeCol);
    tr.appendChild(priceCol);
    tr.classList.add('bought');
    input.parentNode.removeChild(input);
    document.getElementById("listBody").appendChild(tr);

}