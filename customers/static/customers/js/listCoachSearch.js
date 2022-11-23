/**
 * 
 */
var disabled1= document.getElementsByClassName(`navlink_1`);
const onClick =(n)=>{
	let disabled2= document.getElementsByClassName(`navlink_${n}`);
	disabled2.classList.add('disabled');
	console.log(disabled2)
	
}

