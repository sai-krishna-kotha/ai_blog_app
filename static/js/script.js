console.log("I am working");

const blogContent = document.getElementById('blogContent');
const generatedBlock = document.getElementById('generated-block');
const generateBlogButton = document.getElementById('generateBlogButton');
//warning, loading_circle are handled in if block
const warning = document.getElementById('warning-on-process');
const loading_circle = document.getElementById('loading-circle');

const invalid_url_error = document.getElementById('error-invalid-yt-url');
const empty_url_error = document.getElementById('error-empty-yt-url');

window.onload = ()=>{
    generateBlogButton.addEventListener('click', generateHandler);
    invalid_url_error.classList.add('hidden');
    empty_url_error.classList.add('hidden');
}
function disableButton(id) {
    document.getElementById(id).disabled = true;
}
function enableButton(id){
    document.getElementById(id).disabled = false;
}
// scope to implement the cancel button when performing generation
function cancelGeneration(){
    console.log("Perform cancel operation while fetching from server");
    
}
async function generateHandler(event){
    event.preventDefault();
    const youtubeLink = document.getElementById('youtubeLink').value;
    console.log("GENERATE");
    console.log(youtubeLink);
    error_flag = false;
    if (youtubeLink) {
        warning.classList.remove('hidden');
        loading_circle.style.display = 'block';
        disableButton("generateBlogButton");
        generateBlogButton.innerText = 'Cancel';
        generateBlogButton.disabled = true;
        generatedBlock.classList.add('hidden');
        blogContent.innerHTML = ''; // Clear previous content

        const endpointUrl = '/generate-blog/';
        
        try {
            const response = await fetch(endpointUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ link: youtubeLink })
            });
            
            const data = await response.json();
            
            blogContent.innerHTML = data.content;
            
        } catch (error) {
            error_flag = true;
            console.error("Error occurred:", error);
            //alert("Something went wrong. Please try again later.");
            invalid_url_error.classList.remove('hidden')

        }
        loading_circle.style.display = 'none';
        enableButton("generateBlogButton");
        warning.classList.add('hidden');
        generateBlogButton.innerText = 'Generate';

    } else {
        //alert("Please enter a YouTube link.");
        empty_url_error.classList.remove('hidden')
    }
    if (!error_flag)
        generatedBlock.classList.remove('hidden');
}

// document.getElementById('generateBlogButton').addEventListener('click', generateHandler);