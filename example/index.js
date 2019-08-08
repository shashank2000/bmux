const minimist = require('minimist')

module.exports = () => {
    const args = minimist(process.argv.slice(2))
    const cmd = args._[0] || 'help'

    if (args.version || args.v){
        cmd = 'version'
    }

    if (args.help || args.h ){
        cmd = 'help'
    }

    switch(cmd){
        case 'today':
            require('./cmds/today')(args)
            console.log(`cmd is ${cmd}`)
            break
        
        case 'version':
            require('./cmds/version')(args)
            break
        
        case 'help':
            require('./cmds/help')(args)
            break
        
        default:
            console.error(`${cmd} is not a valid command`)
            break
    }
}