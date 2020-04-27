$container_name = 'orders'
$destination_path = 'C:\Users\user\raw_data'
# $connection_string = 'DefaultEndpointsProtocol=https;AccountName=[REPLACEWITHACCOUNTNAME];AccountKey=[REPLACEWITHACCOUNTKEY]'
$storage_account = New-AzStorageContext -ConnectionString $connection_string

$Token = $null
$Total = 0
$StartTime = $(get-date)
DO{
    $blobs = Get-AzStorageBlob -Container $container_name -Context $storage_account -MaxCount 1000 -ContinuationToken $Token 

    if($blobs.Length -le 0) { 
        Break;
    }

    foreach ($blob in $blobs){
        $Total += 1
        $raw_path = Join-Path -Path "C:/Users/user/raw_data/" -ChildPath $blob.Name
        $parsed_path = Join-Path -Path "C:/Users/user/parsed_data/" -ChildPath $blob.Name
        if(-not((Test-Path $raw_path) -or (Test-Path $parsed_path))){
            Get-AzStorageBlobContent -Container $container_name -Blob $blob.Name -Destination $destination_path -Context $storage_account -Force | Out-Null
        }
    }
    
    if(Test-Path C:/Users/user/raw_data/*){
        C:/Users/user/Anaconda3/envs/veritas/python.exe C:/Users/user/Pythia/parser/parser order C:/Users/user/raw_data/*.json C:/Users/user/parsed_data/;
        Remove-Item C:\Users\user\raw_data\*;
    } 
    $Token = $blobs[$blobs.Count -1].ContinuationToken;
    $elapsedTime = $(get-date) - $StartTime
    $totalTime = "{0:HH:mm:ss}" -f ([datetime]$elapsedTime.Ticks)
    
    "Elapsed Time: $totalTime"
    "Total Files: $Total`n"
} While ($Null -ne $Token)

