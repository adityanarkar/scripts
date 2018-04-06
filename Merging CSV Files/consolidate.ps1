#Author: Aditya Narkar

$file1 = Get-Content .\file1.csv
$file2 = Get-Content .\file2.csv
$file3 = Get-Content .\file3.csv

$file1AfterSplit = $file1.Split(",")
$file2AfterSpilt = $file2.Split(",")
$file3AfterSplit = $file3.Split(",")

$fileToConsiderWhileMerging = $file1AfterSplit
# $columnNames = $fileToConsiderWhileMerging[0
$numberOfColumns = #enter number of columns
$i=1
while($fileToConsiderWhileMerging[$i] -lt $numberOfColumns) {
  $columnNames = $columnNames + ", $fileToConsiderWhileMerging[$i]"
  $i += 1
  echo $i
}

$overallresult = $overallresult + $columnNames

$overallresult = $overallresult + "`n"

#for simplicity we'll consider that every csv file contains same number of rows and columns
#if they are of differnet sizes, then simply replace following variable with corresponding file's variable
echo $combine
for($i=$columnNames.length; $i -lt $fileToConsiderWhileMerging.length; $i++) {
  $remainder = $i%$columnNames.length
  if ($remainder -eq 0) { #Entering row value in consolidated csv file
    $row =  $fileToConsiderWhileMerging[$i]
    $overallresult = $overallresult + "`n $row"
  }
  Else {
    $consolidated = $fileToConsiderWhileMerging[$i] + $file2AfterSpilt[$i] + $file3AfterSplit[$i]
    $consolidated -replace ' ', '' #if all sheets has same coordinate blank then replacing it with sing blank
                                   #may be unnecessary but keep it neat and tidy ;)
    if ($consolidated -eq '') {
      $consolidated = ' '
    }
    $overallresult = $overallresult + ", " + $consolidated
  }
}

echo $overallresult
$overallresult >> consolidated.csv
