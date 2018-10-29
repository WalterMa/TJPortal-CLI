#!/bin/bash

req_url='http://192.168.192.10/include/auth_action.php'
cookie_file='login_cookie.txt'

function menu {
    clear
    printf 'Srun4K/Tongji.Portal Command Line Tool\n\n'
    printf ' 1. Login to tongji.portal\n'
    printf ' 2. Fetch current account status\n'
    printf ' 3. Logout from tongji.portal\n'
    printf ' 0. Exit program\n\n'
    printf 'Enter option: '
    read option
}

function portal_login {
    printf '\n1. Login to tongji.portal\n'
    printf 'Please enter your login account info\n'
    read -p 'Username:' s4k_user
    read -sp 'Password:' s4k_pwd
    s4k_pwd='{B}'$(printf $s4k_pwd | base64)
    post_data=$( printf 'action=login&username=%s&password=%s&ac_id=1&user_ip=&nas_ip=&user_mac=&save_me=1&ajax=1' $s4k_user $s4k_pwd )

    printf '\nLogging in...\n'
    curl -sS -c $cookie_file -d $post_data $req_url
}

function portal_logout {
    post_data='action=logout&ajax=1'

    printf '\nLogging out...\n'
    curl -sS -b $cookie_file -c $cookie_file -d $post_data $req_url
}

function account_status {
    post_data='action=get_online_info&ajax=1'

    printf '\nFetching status...\n'
    printf 'used_bytes, used_seconds, user_balance, mac_addr, mac_auth, ip_addr\n'
    curl -sS -b $cookie_file -d $post_data $req_url
}


while true
do

menu

case $option in
0) break 
;;
1) portal_login
;;
2) account_status
;;
3) portal_logout
;;
*) printf '\nWrong option\n'
;;
esac

printf '\n\nPress any key to continue'
read

done