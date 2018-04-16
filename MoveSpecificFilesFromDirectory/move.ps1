$directory = dir -Directory
Foreach ($folder in $directory.Name)
{
    cd $folder
    echo "-----$folder-----"
    $subdirectory = dir -Directory
    Foreach ($subfolder in $subdirectory.Name)
    {
      cd $subfolder
      echo "*****$subfolder*****"
      $r=Get-ChildItem .
      mkdir ..\..\..\logs\$folder+"-"+$subfolder
      $r.name -like "*.log" | ForEach-Object {cp $_ ..\..\..\logs\$folder+"-"+$subfolder}
      # echo $r
      cd ..
    }
    cd ..
  }
