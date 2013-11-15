" Author:  lightxue
" Email:   bkmgtp@gmail.com
" Version: 0.01
" Website: https://github.com/lightxue/SwissCalc

if has('python')
    let scriptdir = expand("<sfile>:h") . '/'
    py import sys
    exe "python sys.path.append('" . scriptdir . "')"
endif

if exists('g:loaded_scalc') || v:version < 700
  finish
endif
let g:loaded_scalc = 1

map <Leader>cl :Calc<CR>

" configurable options
"
if !exists("g:scalc_title")
    let g:scalc_title = "SwissCalc"
endif
if !exists("g:scalc_prompt")
    let g:scalc_prompt = "> "
endif
if !exists("g:scalc_win_size")
    let g:scalc_win_size = 10
endif
if !exists("g:scalc_max_history")
    let g:scalc_max_history = 256
endif
if !exists("g:scalc_cwinsert")
    let g:scalc_cwinsert = 0
endif
if !exists("g:scalc_insert_on_enter")
    let g:scalc_insert_on_enter = 0
endif
if !exists("g:scalc_win_pos")
    let g:scalc_win_pos = 'top' "other possible values: left,right,bottom
endif

command! -nargs=0 -bar Calc call s:scalc_open()

function! s:scalc_open()
    "validate
    let valid = <SID>scalc_validate()
    if valid == -1
        return
    endif

    "if the window is open, jump to it
    let winnum = bufwinnr(g:scalc_title)
    if winnum != -1
        "jump to the existing window
        if winnr() != winnum
            exe winnum . 'wincmd w'
        endif
        return
    endif

    if g:scalc_win_pos =~ "top\\|left"
        let position = 'aboveleft'
    else
        let position = 'rightbelow'
    endif

    "if the buffer does not already exist create otherwise edit.
    let bufnum = bufnr(g:scalc_title)
    if bufnum == -1
        if g:scalc_win_pos =~ "left\\|right"
            let direction = 'vnew' 
        else
            let direction = 'new'
        endif

        let wcmd = direction . ' ' . g:scalc_title
        exe 'silent ' . position . ' ' . g:scalc_win_size . wcmd
        call setline(1, g:scalc_prompt)
    else
        if g:scalc_win_pos =~ "left\\|right"
            let direction = 'vsplit' 
        else
            let direction = 'split'
        endif

        let wcmd = direction . ' +buffer' . bufnum
        exe 'silent ' . position . ' ' . g:scalc_win_size . wcmd
        call setline(line('$'), g:scalc_prompt)
    endif

    let b:scalc_history = []
    let b:scalc_history_idx = -1

    call <SID>scalc_local_setting()
    call <SID>scalc_mappings()
    call <SID>scalc_jump_to_prompt(1)
endfunction

function! s:scalc_local_setting()
    silent! setlocal buftype=nofile
    silent! setlocal nobuflisted
    silent! setlocal noswapfile
    silent! setlocal bufhidden=delete
    silent! setlocal nonumber
    silent! setlocal nowrap
    silent! setlocal nolist
    setlocal filetype=swisscalc
endfunction


function! s:scalc_mappings()
    nnoremap <buffer> <silent> <CR> :call <SID>scalc_repl(0)<CR>
    inoremap <buffer> <silent> <CR> <C-o>:call <SID>scalc_repl(1)<CR>

    "inserting a new line jumps to the prompt
    nmap <buffer> <silent> o :call <SID>scalc_jump_to_prompt(1)<CR>
    nmap <buffer> <silent> O :call <SID>scalc_jump_to_prompt(1)<CR>

    nmap <buffer> <silent> <F1> :help vimcalc-function-list<CR>

    imap <buffer> <silent> <up> <C-o>:call <SID>scalc_pre_cmd()<CR>
    imap <buffer> <silent> <down> <C-o>:call <SID>scalc_next_cmd()<CR>

    au BufEnter <buffer> :call <SID>SCalc_InsertOnEnter()

    call <SId>SCalc_CreateCWInsertMappings()
endfunction

function! s:scalc_validate()
    if has('python') != 1
        echohl WarningMsg | echomsg "SwissCalc requires the Python interface to be installed." | echohl None
        return -1
    endif

    return 0
endfunction

function! s:scalc_repl(continueInsert)

    let s:expr = getline(".")
    if match(s:expr, g:scalc_prompt) != 0
        return
    else
        let s:expr = strpart(s:expr, matchend(s:expr, g:scalc_prompt))
    endif

    call <SID>scalc_record_history(s:expr)
    py repl(vim.eval('s:expr'))

    "if executed command don't continue -- may be a ':q'
    if exists("w:vcalc_vim_command")
        stopinsert
        return
    endif

    let failed = append(line('$'), g:scalc_prompt)

    let b:scalc_history_idx = -1

    call <SID>scalc_jump_to_prompt(a:continueInsert)
endfunction

function! s:scalc_jump_to_prompt(withInsert)
    call setpos(".", [0, line('$'), col('$'), 0])
    if a:withInsert == 1
        startinsert!
    endif
endfunction

function! s:scalc_record_history(expr)
    call insert(b:scalc_history, a:expr)
    if len(b:scalc_history) > g:scalc_max_history
        call remove(b:scalc_history, -1)
    endif
endfunction

function! s:scalc_pre_cmd()
    if b:scalc_history_idx < len(b:scalc_history)-1
        let b:scalc_history_idx += 1
        let failed = setline(line('$'), g:scalc_prompt . b:scalc_history[b:scalc_history_idx])
        call <SID>scalc_jump_to_prompt(1)
    endif
endfunction

function! s:scalc_next_cmd()
    if b:scalc_history_idx > 0
        let b:scalc_history_idx -= 1
        let failed = setline(line('$'), g:scalc_prompt . b:scalc_history[b:scalc_history_idx])
        call <SID>scalc_jump_to_prompt(1)
    endif
endfunction

function! s:SCalc_InsertOnEnter()
    if g:scalc_insert_on_enter
        call <SID>scalc_jump_to_prompt(1)
    endif
endfunction

function! s:SCalc_CreateCWInsertMappings()
    if g:scalc_cwinsert
        imap <buffer> <silent> <C-W>l <ESC><C-W>l
        imap <buffer> <silent> <C-W>k <ESC><C-W>k
        imap <buffer> <silent> <C-W>j <ESC><C-W>j
        imap <buffer> <silent> <C-W>h <ESC><C-W>h
        imap <buffer> <silent> <C-W>b <ESC><C-W>b
        imap <buffer> <silent> <C-W>t <ESC><C-W>t
        imap <buffer> <silent> <C-W>w <ESC><C-W>w
        imap <buffer> <silent> <C-W>W <ESC><C-W>W
        "for lazy fingers:
        imap <buffer> <silent> <C-W><c-l> <ESC><C-W>l
        imap <buffer> <silent> <C-W><c-k> <ESC><C-W>k
        imap <buffer> <silent> <C-W><c-j> <ESC><C-W>j
        imap <buffer> <silent> <C-W><c-h> <ESC><C-W>h
        imap <buffer> <silent> <C-W><c-b> <ESC><C-W>b
        imap <buffer> <silent> <C-W><c-t> <ESC><C-W>t
        imap <buffer> <silent> <C-W><c-w> <ESC><C-W>w
        imap <buffer> <silent> <C-W><c-W> <ESC><C-W>W
    endif
endfunction

" **********************************************************************************************************
" **** PYTHON **********************************************************************************************
" **********************************************************************************************************

if has('python')

python << EOF

import vim
import swisscalc

calc = swisscalc.Calc(debug=0)

funcs = r'\\|'.join(r'\\<%s\\>' % func for func in calc.funcs)
vim.command('let g:scalc_funcs = "%s"' % funcs)
ops = ['+', '-', r'\\*', '/', '%', r'\\*\\*', '!', '<<', '>>', '&',
       r'\\~', '|', r'\\^', '=', '+=', '-=', r'\\*=', '/=', '%=',
       r'\\*\\*=', '<<=', '>>=', '&=', '|=', r'\\^=']
ops = r'\\|'.join(ops)
vim.command('let g:scalc_ops = "%s"' % ops)

def repl(expr):
    expr = expr.strip()
    if not expr:
        return
    result = calc.execute(expr)
    if not result:
        return
    for line in result.split('\n'):
        vim.current.buffer.append(line + '\n')
    vim.command('if exists("w:vcalc_vim_command") | unlet w:vcalc_vim_command | endif')
EOF

endif
