const getYear = () => {
  return new Date().getFullYear();
};

document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("current-year").textContent = getYear();
});

const dropArea = document.getElementById("drop-area");
const droprAreaMsg = document.querySelector('#drop-area');
const input = document.querySelector('input');

const errorText = document.querySelector('#error-text');

dropArea.addEventListener('click', (e) => {
  input.click();
  input.onchange = (e) => {
    upload(e.target.files);
  }
});

dropArea.addEventListener('dragover', (e) => {
  e.preventDefault();
});

dropArea.addEventListener("drop", async (e) => { 
  e.preventDefault();
  
  if (![...e.dataTransfer.items].every((item) => item.kind === 'file')) {
    errorText.textContent = "Error: Not a file or files";
    throw new Error("Not a file or files");
  }

  // if (e.dataTransfer.items.length > 1) {
  //   errorText.textContent = "Error: Cannot upload multiple files";
  //   throw new Error("Multiole items");
  // }

  const filesArray = [...e.dataTransfer.files];

  const areFiles = await Promise.all([...e.dataTransfer.files].map((file) => {
    return new Promise((resolve) => {
      const fr = new FileReader();
      fr.onprogress = (e) => {
        if (e.loaded > 50) {
          fr.abort();
          resolve(true);
        }
      }
      fr.onload = () => { resolve(true); }
      fr.onerror = () => { resolve(false); }
      fr.readAsArrayBuffer(file);
    });
  }));

  if (!areFiles.every(item => item === true)) {
    errorText.textContent = "Error: Not a file or files (cannot be a folder)";
    throw new Error("Couldn't read file");
  }

  upload(filesArray);
});

function upload(files) {
  
  const fd = new FormData();
  for (let i=0; i<files.length; i++) {
    fd.append('file${i+1}', files[i]);
  }

  droprAreaMsg.textContent = "Uploading...";

  const req = new XMLHttpRequest();
  req.open('POST', 'http://httpbin.org/post');

  req.upload.addEventListener('progress', (e) => {
    const progress = e.loaded / e.total;
    droprAreaMsg.textContent = (progress*100).toFixed()+"%";
    if (progress === 1) {
      droprAreaMsg.textContent = "Processing...";
    }
  });

  req.addEventListener('load', () => {
    if (req.status === 200) {
      const file = files[0];
      const reader = new FileReader();
    
      reader.onload = (e) => {
        dropArea.style.backgroundImage = `url(${e.target.result})`;
        dropArea.style.backgroundSize = 'cover';
        dropArea.style.backgroundPosition = 'center';
      };

      reader.readAsDataURL(file);
      
      droprAreaMsg.textContent = "File uploaded successfully";
      console.log(JSON.parse(req.responseText));
    } else {
      errorText.textContent = "Upload failed";
      console.error("Bad response");
    }
  });

  req.addEventListener('error', () => {
    errorText.textContent = "Error: Could not upload file";
    console.error("Network Error: Could not upload file");
  });

  req.send(fd);

}