<?php

   $errors = []; 
   $fileFormats = ['jpeg','jpg','png']; 
   $fileName = $_FILES['file']['name'];
   $fileSize = $_FILES['file']['size'];
   $fileTmpName  = $_FILES['file']['tmp_name'];
   $fileType = $_FILES['file']['type'];
   $fileExtension = strtolower(end(explode('.',$fileName)));

        if (! in_array($fileExtension,$fileFormats)) {
            $errors[] = "This file extension is not allowed, please 
            try again";
        }

        if ($fileSize > 5000000){
            $errors[] = "The file size is more than 5 mb, please try again
         with a less sized file";
        }

         if (empty($errors)){
            echo "upload successful";
          } else{
            foreach ($errors as $error) {
                echo $error . "These are the errors" . "\n";
            }
         }  



?>