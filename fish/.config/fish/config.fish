if status is-interactive
# Commands to run in interactive sessions can go here
set -U fish_greeting
neofetch
fish_add_path /opt/homebrew/bin
starship init fish | source
function ls
    nu -c "ls $argv"
end
end
