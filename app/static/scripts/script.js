const getYear = () => { 
  return new Date().getFullYear();
};

document.addEventListener("DOMContentLoaded", () => { 
  document.getElementById("current-year").textContent = getYear();
});


const dropImage = document.getElementById("drop-image");
const dropImageMsg = document.querySelector('#placeholder-text');
const input = document.querySelector('input');

const errorText = document.querySelector('#error-text');

// Подія на клік по області перетягування
dropImage.addEventListener('click', (e) => { 
  input.click(); // Імітуємо клік по інпуту для вибору файлів
  input.onchange = (e) => { 
    upload(e.target.files); // Завантажуємо файли після вибору
  }
});

//  Для перетягування файлів
dropImage.addEventListener('dragover', (e) => { 
  e.preventDefault();
});

// Для скидання файлів в область перетягування
dropImage.addEventListener("drop", async (e) => { 
  e.preventDefault();
  
  // Перевірка, чи всі елементи є файлами
  if (![...e.dataTransfer.items].every((item) => item.kind === 'file')) { 
    errorText.textContent = "Помилка: не файл або файли"; // Виводимо помилку
    throw new Error("Не файл або файли"); // Кидаємо помилку
  }

  // Перетворюємо список файлів на масив
  const filesArray = [...e.dataTransfer.files]; 

  // Перевіряємо, чи всі файли можна прочитати
  const areFiles = await Promise.all([...e.dataTransfer.files].map((file) => { 
    return new Promise((resolve) => { 
      const fr = new FileReader();
      fr.onprogress = (e) => { 
        if (e.loaded > 50) { // Якщо файл завантажується більше 50%
          fr.abort(); // Припиняємо читання файлу
          resolve(true); // Підтверджуємо, що файл валідний
        }
      }
      fr.onload = () => { resolve(true); } // Якщо файл успішно завантажений
      fr.onerror = () => { resolve(false); } // Якщо сталася помилка при завантаженні
      fr.readAsArrayBuffer(file); // Читаємо файл як масив байтів
    });
  }));

  // Якщо хоча б один файл не можна прочитати, виводимо помилку
  if (!areFiles.every(item => item === true)) { 
    errorText.textContent = "Помилка: не файл або файли (не може бути папкою)"; // Повідомлення про помилку
    throw new Error("Не вдалося прочитати файл"); // Кидаємо помилку
  }

  // Завантажуємо файли, якщо всі файли валідні
  upload(filesArray); 
});

// Функція для завантаження файлів на сервер
function upload(files) { 
  const fd = new FormData(); // Створюємо нову форму для відправки файлів
  for (let i=0; i<files.length; i++) { 
    fd.append('file${i+1}', files[i]); // Додаємо файл до форми з індексом
  }

  dropImageMsg.textContent = "Завантаження...";

  const req = new XMLHttpRequest(); // Створюємо новий запит
  req.open('POST', 'http://httpbin.org/post'); // Відкриваємо POST-запит

  // Обробка прогресу завантаження
  req.upload.addEventListener('progress', (e) => { 
    const progress = e.loaded / e.total; // Обчислюємо відсоток завантаженого контенту
    dropImageMsg.textContent = (progress*100).toFixed() + "%"; // Виводимо відсоток прогресу
    if (progress === 1) { 
      dropImageMsg.textContent = "Обробка...";
    }
  });


  // Обробка відповіді від сервера
  req.addEventListener('load', () => { 
    if (req.status === 200) {
      const file = files[0]; // Вибираємо перший файл
      const reader = new FileReader(); // Створюємо FileReader для читання файлу
      let uploadedImageData = null;

      reader.onload = (e) => { 
        uploadedImageData = e.target.result; // Зберігаємо зображення у змінній
        
        console.log(uploadedImageData);

        fetch('http://127.0.0.1:5000/blog/post', {
          method: "POST",
          body: JSON.stringify({ imageData: uploadedImageData}),
          headers:{
                  'Accept': 'application/json'
          },
        })
        .then(function(response) {
          if (response.status !== 200) {
            console.log('Response status not 200:', response.status)
            return ;
          }
          response.json().then(function(data) {
            console.log(data)
          })
        })
        .catch((error) => console.error("Помилка:", error));

        dropImage.style.backgroundImage = `url(${uploadedImageData})`; // Встановлюємо зображення в якості фону
        dropImage.style.backgroundSize = 'cover';
        dropImage.style.backgroundPosition = 'center';
      };

      reader.readAsDataURL(file); // Читаємо файл як Data URL
      
      dropImageMsg.textContent = "Файл успішно завантажено"; 
      console.log(JSON.parse(req.responseText)); // Логуємо відповідь сервера
    } else { 
      errorText.textContent = "Помилка завантаження";
      console.error("Погана відповідь");
    }
  });

  // Обробка помилок запиту
  req.addEventListener('error', () => { 
    errorText.textContent = "Помилка: не вдалося завантажити файл";
    console.error("Помилка мережі: не вдалося завантажити файл");
  });

  req.send(fd); // Відправляємо запит на сервер з формою
}