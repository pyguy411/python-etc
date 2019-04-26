hack to make your self local admin on your machien.
open PowerSheell as administrator with Defendpoint

enter those two commands

    Add-LocalGroupMember -Group Administrators -Member <yourguid>
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Force
    
