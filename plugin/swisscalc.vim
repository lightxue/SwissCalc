" Author:  lightxue
" Email:   bkmgtp@gmail.com
" Version: 0.01
" Website: https://github.com/lightxue/SwissCalc

if has('python')
    let scriptdir = expand("<sfile>:h") . '/'
    py import sys
    exe "python sys.path.append('" . scriptdir . "')"
endif

if exists('g:loaded_swisscalc') || v:version < 700
  finish
endif
let g:loaded_swisscalc = 1

map <Leader>cl :Calc<CR>

" configurable options
"
if !exists("g:SwissCalc_Title")
    let g:SwissCalc_Title = "SwissCalc"
endif
if !exists("g:SwissCalc_Prompt")
    let g:SwissCalc_Prompt = "> "
endif
if !exists("g:SwissCalc_Win_Size")
    let g:SwissCalc_Win_Size = 10
endif
if !exists("g:SwissCalc_Max_History")
    let g:SwissCalc_Max_History = 256
endif
if !exists("g:SwissCalc_CWInsert")
    let g:SwissCalc_CWInsert = 0
endif
if !exists("g:SwissCalc_InsertOnEnter")
    let g:SwissCalc_InsertOnEnter = 0
endif
if !exists("g:SwissCalc_WindowPosition")
    let g:SwissCalc_WindowPosition = 'top' "other possible values: left,right,bottom
endif

command! -nargs=0 -bar Calc call s:SCalc_Open()

function! s:SCalc_Open()
    "validate
    let valid = <SID>SCalc_ValidateVim()
    if valid == -1
        return
    endif

    "if the window is open, jump to it
    let winnum = bufwinnr(g:SwissCalc_Title)
    if winnum != -1
        "jump to the existing window
        if winnr() != winnum
            exe winnum . 'wincmd w'
        endif
        return
    endif

    if g:SwissCalc_WindowPosition =~ "top\\|left"
        let position = 'aboveleft'
    else
        let position = 'rightbelow'
    endif

    "if the buffer does not already exist create otherwise edit.
    let bufnum = bufnr(g:SwissCalc_Title)
    if bufnum == -1
        if g:SwissCalc_WindowPosition =~ "left\\|right"
            let direction = 'vnew' 
        else
            let direction = 'new'
        endif

        let wcmd = direction . ' ' . g:SwissCalc_Title
        exe 'silent ' . position . ' ' . g:SwissCalc_Win_Size . wcmd
        call setline(1, g:SwissCalc_Prompt)
    else
        if g:SwissCalc_WindowPosition =~ "left\\|right"
            let direction = 'vsplit' 
        else
            let direction = 'split'
        endif

        let wcmd = direction . ' +buffer' . bufnum
        exe 'silent ' . position . ' ' . g:SwissCalc_Win_Size . wcmd
        call setline(line('$'), g:SwissCalc_Prompt)
    endif

    let b:SwissCalc_History = []
    let b:SwissCalc_History_Index = -1

    call <SID>SCalc_SetLocalSettings()
    call <SID>SCalc_DefineMappingsAndAutoCommands()
    call <SID>SCalc_JumpToPrompt(1)
endfunction

function! s:SCalc_SetLocalSettings()
    silent! setlocal buftype=nofile
    silent! setlocal nobuflisted
    silent! setlocal noswapfile
    silent! setlocal bufhidden=delete
    silent! setlocal nonumber
    silent! setlocal nowrap
    silent! setlocal nolist
    setlocal filetype=swisscalc
endfunction


function! s:SCalc_DefineMappingsAndAutoCommands()
    nnoremap <buffer> <silent> <CR> :call <SID>SCalc_REPL(0)<CR>
    inoremap <buffer> <silent> <CR> <C-o>:call <SID>SCalc_REPL(1)<CR>

    "inserting a new line jumps to the prompt
    nmap <buffer> <silent> o :call <SID>SCalc_JumpToPrompt(1)<CR>
    nmap <buffer> <silent> O :call <SID>SCalc_JumpToPrompt(1)<CR>

    nmap <buffer> <silent> <F1> :help vimcalc-function-list<CR>

    imap <buffer> <silent> <up> <C-o>:call <SID>SCalc_PreviousHistory()<CR>
    imap <buffer> <silent> <down> <C-o>:call <SID>SCalc_NextHistory()<CR>

    au BufEnter <buffer> :call <SID>SCalc_InsertOnEnter()

    call <SId>SCalc_CreateCWInsertMappings()
endfunction

function! s:SCalc_ValidateVim()
    if has('python') != 1
        echohl WarningMsg | echomsg "SwissCalc requires the Python interface to be installed." | echohl None
        return -1
    endif

    return 0
endfunction

function! s:SCalc_REPL(continueInsert)

    let s:expr = getline(".")
    if match(s:expr, g:SwissCalc_Prompt) != 0
        return
    else
        let s:expr = strpart(s:expr, matchend(s:expr, g:SwissCalc_Prompt))
    endif

    call <SID>SCalc_RecordHistory(s:expr)
    py repl(vim.eval('s:expr'))

    "if executed command don't continue -- may be a ':q'
    if exists("w:vcalc_vim_command")
        stopinsert
        return
    endif

    let failed = append(line('$'), g:SwissCalc_Prompt)

    let b:SwissCalc_History_Index = -1

    call <SID>SCalc_JumpToPrompt(a:continueInsert)
endfunction

function! s:SCalc_JumpToPrompt(withInsert)
    call setpos(".", [0, line('$'), col('$'), 0])
    if a:withInsert == 1
        startinsert!
    endif
endfunction

function! s:SCalc_RecordHistory(expr)
    call insert(b:SwissCalc_History, a:expr)
    if len(b:SwissCalc_History) > g:SwissCalc_Max_History
        call remove(b:SwissCalc_History, -1)
    endif
endfunction

function! s:SCalc_PreviousHistory()
    if b:SwissCalc_History_Index < len(b:SwissCalc_History)-1
        let b:SwissCalc_History_Index += 1
        let failed = setline(line('$'), g:SwissCalc_Prompt . b:SwissCalc_History[b:SwissCalc_History_Index])
        call <SID>SCalc_JumpToPrompt(1)
    endif
endfunction

function! s:SCalc_NextHistory()
    if b:SwissCalc_History_Index > 0
        let b:SwissCalc_History_Index -= 1
        let failed = setline(line('$'), g:SwissCalc_Prompt . b:SwissCalc_History[b:SwissCalc_History_Index])
        call <SID>SCalc_JumpToPrompt(1)
    endif
endfunction

function! s:SCalc_InsertOnEnter()
    if g:SwissCalc_InsertOnEnter
        call <SID>SCalc_JumpToPrompt(1)
    endif
endfunction

function! s:SCalc_CreateCWInsertMappings()
    if g:SwissCalc_CWInsert
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
