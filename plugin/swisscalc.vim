" Author:  lightxue
" Email:   bkmgtp@gmail.com
" Version: 0.01
" Website: https://github.com/lightxue/SwissCalc

"{{{ Init
if exists('g:loaded_scalc') || v:version < 700
    finish
endif
let g:loaded_scalc = 1
"}}}

"{{{ Misc
command! -nargs=0 Scalc       call swisscalc#ScalcOpen('')
command! -nargs=0 ScalcSplit  call swisscalc#ScalcOpen('topleft split')
command! -nargs=0 ScalcVSplit call swisscalc#ScalcOpen('topleft vsplit')
command! -nargs=0 ScalcTab    call swisscalc#ScalcOpen('tabnew')
"}}}

" vim: foldmethod=marker shiftwidth=4

