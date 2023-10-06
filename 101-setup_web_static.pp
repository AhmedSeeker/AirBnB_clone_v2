#Redo task 0 by using Puppet

exec {'directories':
  command  => 'sudo mkdir -p /data/web_static/releases/test/; sudo mkdir -p /data/web_static/shared/',
  provider => shell,
}

-> file {'/data/web_static/releases/test/index.html':
  ensure  => file,
  content => "<html>\n  <head>\n  </head>\n  <body>\n    Holberton School\n  </body>\n</html>\n",
  require => Exec['directories'],
}

file {'/data/web_static/current':
  ensure  => link,
  target  => '/data/web_static/releases/test',
  require => Exec['directories'],
}

exec {'ubuntu':
  command  => 'sudo chown -R ubuntu:ubuntu /data/',
  provider => shell,
  require  => Exec['directories'],
}

exec {'sudo apt-get update':
  provider => shell,
  notify   => Package['nginx'],
}

package {'nginx':
  ensure   => installed,
  provider => apt,
  require  => Exec['sudo apt-get update'],
}

file_line {'hbnb_static':
  ensure  => present,
  line    => "\n\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}",
  after   => '^\troot /var/www/html;',
  path    => '/etc/nginx/sites-available/default',
  require => Package['nginx'],
  notify  => Service['nginx'],
}

service {'nginx':
  ensure => running,
}
