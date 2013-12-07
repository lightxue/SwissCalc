" Author:  lightxue
" Email:   bkmgtp@gmail.com
" Version: 0.01
" Website: https://github.com/lightxue/SwissCalc

"{{{ Init

if version < 700 "{{{
    function! s:ScalcDidNotLoad()
        echohl WarningMsg
        echomsg "SwissCalc unavailable: requires Vim 7.0+"
        echohl None
    endfunction
    command! -nargs=0 SCalc call s:ScalcDidNotLoad()
    finish
endif "}}}

if has('python') "{{{
    let s:script_path = expand("<sfile>:h")
    py import sys
    py sys.path.append(vim.eval('s:script_path'))

else
    function! s:ScalcDidNotLoad()
        echohl WarningMsg
        echomsg "SwissCalc unavailable: requires Python2.7+"
        echohl None
    endfunction
    command! -nargs=0 SCalc call s:ScalcDidNotLoad()
    finish
endif "}}}

"{{{ configurable options
if !exists("g:scalc_title")
    let g:scalc_title = "__SwissCalc__"
endif
if !exists("g:scalc_prompt")
    let g:scalc_prompt = "> "
endif
if !exists("g:scalc_max_history")
    let g:scalc_max_history = 256
endif
"}}}

"}}}

"{{{ Interface

function! swisscalc#ScalcOpen(open_cmd) "{{{
    call s:scalc_open(a:open_cmd)
endfunction "}}}

function! swisscalc#ScalcPreCmd() "{{{
    call s:scalc_pre_cmd()
endfunction "}}}

function! swisscalc#ScalcNextCmd() "{{{
    call s:scalc_next_cmd()
endfunction "}}}

"}}}

"{{{ Util

function! s:scalc_jump_to_prompt(insert_mode) "{{{
    if match(getline('$'), g:scalc_prompt) != 0
        call append(line('$'), g:scalc_prompt)
    endif
    call setpos(".", [0, line('$'), col('$'), 0])
    if a:insert_mode == 1
        startinsert!
    endif
endfunction "}}}

"}}}

"{{{ Buffer

function! s:scalc_open(open_cmd) "{{{

    silent! exe a:open_cmd
    let bufnum = bufnr(g:scalc_title)
    if bufnum == -1
        silent exe 'edit ' . g:scalc_title
    else
        silent exe 'buffer ' . bufnum
    endif

    call setline(line('$'), g:scalc_prompt)

    let b:scalc_history = []
    let b:scalc_history_idx = -1

    call <SID>scalc_local_setting()
    call <SID>scalc_mappings()
    call <SID>scalc_jump_to_prompt(1)
endfunction
"}}}

function! s:scalc_local_setting() "{{{
    silent! setlocal fileencoding=utf-8
    silent! setlocal buftype=nofile
    silent! setlocal nobuflisted
    silent! setlocal noswapfile
    silent! setlocal bufhidden=delete
    silent! setlocal nonumber
    silent! setlocal nowrap
    silent! setlocal noswapfile
    silent! setlocal nolist
    silent! setlocal filetype=swisscalc
endfunction "}}}

function! s:scalc_mappings() "{{{
    nnoremap <buffer> <silent> <CR> :call <SID>scalc_repl(0)<CR>
    inoremap <buffer> <silent> <CR> <C-o>:call <SID>scalc_repl(1)<CR>

    " inserting a new line jumps to the prompt
    nnoremap <buffer> <silent> o :call <SID>scalc_jump_to_prompt(1)<CR>
    nnoremap <buffer> <silent> O :call <SID>scalc_jump_to_prompt(1)<CR>

    nnoremap <buffer> <silent> <F1> :help swisscalc-usage<CR>

    inoremap <buffer> <silent> <up> <C-o>:call <SID>scalc_pre_cmd()<CR>
    inoremap <buffer> <silent> <down> <C-o>:call <SID>scalc_next_cmd()<CR>

    inoremap <buffer> <silent> <C-p> <C-o>:call <SID>scalc_pre_cmd()<CR>
    inoremap <buffer> <silent> <C-n> <C-o>:call <SID>scalc_next_cmd()<CR>

endfunction "}}}

function! s:scalc_repl(insert_mode) "{{{

    let s:expr = getline(".")
    if match(s:expr, g:scalc_prompt) != 0
        return
    endif

    let s:expr = strpart(s:expr, matchend(s:expr, g:scalc_prompt))

    call <SID>scalc_record_cmd(s:expr)
    py repl(vim.eval('s:expr'))

    let failed = append(line('$'), g:scalc_prompt)

    let b:scalc_history_idx = -1

    call <SID>scalc_jump_to_prompt(a:insert_mode)

endfunction "}}}

"}}}

"{{{ History

function! s:scalc_record_cmd(expr) "{{{
    call insert(b:scalc_history, a:expr)
    if len(b:scalc_history) > g:scalc_max_history
        call remove(b:scalc_history, -1)
    endif
endfunction "}}}

function! s:scalc_pre_cmd() "{{{
    if b:scalc_history_idx < len(b:scalc_history)-1
        let b:scalc_history_idx += 1
        let failed = setline(line('$'), g:scalc_prompt . b:scalc_history[b:scalc_history_idx])
        call <SID>scalc_jump_to_prompt(1)
    endif
endfunction "}}}

function! s:scalc_next_cmd() "{{{
    if b:scalc_history_idx > 0
        let b:scalc_history_idx -= 1
        let failed = setline(line('$'), g:scalc_prompt . b:scalc_history[b:scalc_history_idx])
        call <SID>scalc_jump_to_prompt(1)
    endif
endfunction "}}}

"}}}

"{{{ Python

if has('python')

python << EOF

import vim
import swisscalc

calc = swisscalc.Calc(vim.eval('s:script_path'))

# function list
funcs = r'\\|'.join(r'\\<%s\\>' % func for func in calc.funcs)
vim.command('let g:scalc_funcs = "%s"' % funcs)

# operator list
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
EOF

endif

"}}}

" vim: foldmethod=marker shiftwidth=4

