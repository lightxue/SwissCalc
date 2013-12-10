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
    command! -nargs=0 SCalc       call s:ScalcDidNotLoad()
    command! -nargs=0 SCalcSplit  call s:ScalcDidNotLoad()
    command! -nargs=0 SCalcVSplit call s:ScalcDidNotLoad()
    command! -nargs=0 SCalcTab    call s:ScalcDidNotLoad()
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
    let g:scalc_max_history = 1024
endif
if !exists("g:scalc_save_history")
    let g:scalc_have_history = 1
endif
"}}}

"{{{ event registe
exe 'au BufNewFile '. g:scalc_title . ' py his.load_cmds()'
exe 'au VimLeave,BufLeave '. g:scalc_title . ' py his.save_cmds()'
"}}}

"}}}

"{{{ Interface

function! swisscalc#ScalcOpen(open_cmd) "{{{
    call s:scalc_open(a:open_cmd)
endfunction "}}}

function! swisscalc#ScalcToggleBin() "{{{
    py calc.execute(("setenv('bin')"))
endfunction "}}}

function! swisscalc#ScalcToggleDec() "{{{
    py calc.execute(("setenv('dec')"))
endfunction "}}}

function! swisscalc#ScalcToggleHex() "{{{
    py calc.execute(("setenv('hex')"))
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

    call <SID>scalc_local_setting()
    call <SID>scalc_mappings()
    py his.jump_to_prompt(True)
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

    nnoremap <buffer> <silent> <CR> :py repl(0)<CR>
    inoremap <buffer> <silent> <CR> <C-o>:py repl(1)<CR>

    " inserting a new line jumps to the prompt
    nnoremap <buffer> <silent> o :call <SID>scalc_jump_to_prompt(1)<CR>
    nnoremap <buffer> <silent> O :call <SID>scalc_jump_to_prompt(1)<CR>

    " exit
    inoremap <buffer> <silent> <C-D> <Esc>:q<CR>

    " help
    nnoremap <buffer> <silent> <F1> :help swisscalc-usage<CR>

    " history
    inoremap <buffer> <silent> <up> <C-o>:py his.pre_cmd()<CR>
    inoremap <buffer> <silent> <down> <C-o>:py his.next_cmd()<CR>

    inoremap <buffer> <silent> <C-P> <C-o>:py his.pre_cmd()<CR>
    inoremap <buffer> <silent> <C-N> <C-o>:py his.next_cmd()<CR>

endfunction "}}}

"}}}

"{{{ Python

if has('python')

python << EOF

import vim
import swisscalc
import history

calc = swisscalc.Calc(vim.eval('s:script_path'))
his = history.History(vim.eval('s:script_path'))

# function list
funcs = r'\|'.join(r'\<%s\>' % func for func in calc.funcs)
vim.vars['scalc_funcs'] = funcs

# operator list
ops = ['+', '-', r'\*', '/', '//', '%', r'\*\*', '!', '<<', '>>', '&',
       r'\~', '|', r'\^', '=', '+=', '-=', r'\*=', '/=', '%=',
       r'\*\*=', '<<=', '>>=', '&=', '|=', r'\^=']
ops = r'\|'.join(ops)
vim.vars['scalc_ops'] = ops

def repl(insert_mode):
    line = vim.current.line
    prompt = vim.vars['scalc_prompt']

    while True:
        if not line.startswith(prompt):
            break

        expr = line[len(prompt):].strip()
        if not expr:
            break

        his.record_cmd(expr)
        result = calc.execute(expr)
        if not result:
            break
        for line in result.split('\n'):
            vim.current.buffer.append(line + '\n')

    vim.current.buffer.append(prompt)
    his.jump_to_prompt(insert_mode)

EOF

endif " has('python')

"}}}

" vim: foldmethod=marker shiftwidth=4

