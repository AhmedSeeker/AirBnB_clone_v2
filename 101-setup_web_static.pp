#using Puppet

exec {'apt_update':
  command  => 'sudo apt update',
  provider => shell,
}

package {'nginx':
  ensure   => installed,
  provider => apt,
  require  => Exec['apt_update'],
}

exec {'data':
  command  => 'sudo mkdir -p /data/web_static/releases/test/; mkdir -p /data/web_static/shared/',
  provider => shell,
}

file {'index html':
  ensure  => file,
  path    => '/data/web_static/releases/test/index.html',
  require => Exec['data'],
  content => "<html>\n  <head>\n  </head>\n  <body>\n    Holberton School\n  </body>\n</html>\n",
}

file {'symbol link':
  ensure  => link,
  path    => '/data/web_static/current',
  target  => '/data/web_static/releases/test',
  require => File['index html'],
}

exec {'mode':
  command  => 'sudo chown -R ubuntu:ubuntu /data/',
  provider => shell,
  require  => File['symbol link'],
}

file_line {'default':
  ensure  => present,
  path    => '/etc/nginx/sites-available/default',
  line    => "\n\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}",
  after   => '^\troot /var/www/html;',
  require => Package['nginx'],
  notify  => Service['nginx'],
}

service {'nginx':
  ensure => running
}
