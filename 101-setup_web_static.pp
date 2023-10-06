#using Puppet

exec {'apt_update':
  command  => 'sudo apt update',
  provider => shell,
}

-> package {'nginx':
  ensure   => installed,
  provider => apt,
  require  => Exec['apt_update'],
}

-> exec {'data':
  command  => 'sudo mkdir -p /data/web_static/releases/test/; mkdir -p /data/web_static/shared/',
  provider => shell,
}

-> file {'/data/web_static/releases/test/index.html':
  ensure  => file,
  require => Exec['data'],
  content =>"<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>
",
}

-> exec {'link':
  command  => 'sudo ln -sf /data/web_static/releases/test /data/web_static/current',
  provider => shell,
}

-> exec {'mode':
  command  => 'chown -R ubuntu:ubuntu /data/',
  provider => shell,
}

-> exec {'header':
  command  => "sudo sed -i '\\%^\\tlocation / %i\\\\tlocation /hbnb_static/ {alias /data/web_static/current/;}\\n'\
 /etc/nginx/sites-available/default",
  provider => shell,
  require  => Package['nginx'],
}

-> exec {'restart':
  command  => 'sudo service nginx restart',
  provider => shell,
  require  => Exec['header'],
}
